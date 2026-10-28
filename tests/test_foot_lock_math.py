"""Pure-math regression checks for Motion2MixamoRig foot planting.

No SMPL-X / Mixamo FBX / GVHMR weights required.
These checks do not substitute for animated-mesh / commercial-license QA.
"""
import unittest

import numpy as np

from motion2mixamorig.mixamo.foot_lock import (
    contact_mask,
    correction_track,
    hip_reach_delta,
    segments,
    two_bone_ik,
)
from motion2mixamorig.mixamo.ground import support_delta_m


class ContactTests(unittest.TestCase):
    def test_contact_hysteresis_and_minimum_duration(self):
        # Enter >= 0.8; remain on >= 0.5; 3 frames at 30 fps qualify.
        confidence = np.array([0.0, 0.9, 0.6, 0.7, 0.4, 0.9, 0.3, 0.0])
        expected = np.array([False, True, True, True, False, False, False, False])
        np.testing.assert_array_equal(contact_mask(confidence, 30), expected)

    def test_segments_exclusive_end(self):
        self.assertEqual(segments(np.array([False, True, True, False, True, False])), [(1, 3), (4, 5)])
        self.assertEqual(segments(np.zeros(5, dtype=bool)), [])

    def test_correction_pins_stationary_contact(self):
        positions = np.stack([np.arange(7, dtype=float), np.zeros(7), np.zeros(7)], axis=-1)
        planted = np.array([False, True, True, True, True, False, False])
        offset, weight = correction_track(positions, planted, blend=3)
        anchored = positions + offset
        np.testing.assert_allclose(anchored[1:5, 0], np.full(4, 2.5), atol=1e-10)
        np.testing.assert_array_equal(weight[1:5], np.ones(4))
        self.assertTrue(np.all((weight >= 0) & (weight <= 1)))


class ReachTests(unittest.TestCase):
    def test_reach_has_zero_shift_when_inside(self):
        shift = hip_reach_delta([(np.array([0.3, 0.0, 0.0]), 1.0)])
        np.testing.assert_allclose(shift, [0.0, 0.0, 0.0], atol=1e-10)

    def test_reach_minimum_shift_one_leg(self):
        shift = hip_reach_delta([(np.array([3.0, 0.0, 0.0]), 1.0)])
        np.testing.assert_allclose(shift, [2.0, 0.0, 0.0], atol=1e-10)

    def test_two_bone_ik_targets_reachable_point(self):
        hip = np.array([0.0, 0.0, 0.0])
        knee = np.array([0.0, -1.0, 0.0])
        ankle = np.array([0.0, -2.0, 0.0])
        target = np.array([0.2, -1.4, 0.0])
        thigh, shin, unreachable = two_bone_ik(hip, knee, ankle, target, np.array([0, 0, 1]))
        self.assertFalse(unreachable)
        solved_knee = hip + thigh @ (knee - hip)
        solved_ankle = solved_knee + shin @ thigh @ (ankle - knee)
        np.testing.assert_allclose(solved_ankle, target, atol=1e-6)
        np.testing.assert_allclose(thigh @ thigh.T, np.eye(3), atol=1e-6)
        np.testing.assert_allclose(shin @ shin.T, np.eye(3), atol=1e-6)

    def test_two_bone_ik_marks_out_of_reach(self):
        thigh, shin, unreachable = two_bone_ik(
            np.array([0.0, 0.0, 0.0]),
            np.array([0.0, -1.0, 0.0]),
            np.array([0.0, -2.0, 0.0]),
            np.array([0.0, -3.0, 0.0]),
            np.array([0, 0, 1]),
        )
        self.assertTrue(unreachable)
        self.assertTrue(np.isfinite(thigh).all() and np.isfinite(shin).all())


class GroundTests(unittest.TestCase):
    def test_support_ground_shift_uses_lowest_frame_in_plant(self):
        heights = np.full((7, 4), np.nan)
        heights[:, 0] = np.array([0.0, -0.08, -0.10, -0.06, 0.0, 0.0, 0.0])
        contact = np.zeros((7, 4))
        contact[1:4, 0] = 0.99
        shift = support_delta_m(heights, contact, fps=30)
        np.testing.assert_allclose(shift, np.full(7, 0.1), atol=1e-10)

    def test_no_plant_no_ground_correction(self):
        heights = np.full((7, 4), 0.2)
        contact = np.zeros((7, 4))
        np.testing.assert_allclose(
            support_delta_m(heights, contact, fps=30), np.zeros(7), atol=1e-10
        )


if __name__ == "__main__":
    unittest.main()

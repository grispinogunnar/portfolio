def get_squat_feedback(knee_angle, min_depth=90):
    """
    Provide feedback based on the knee angle during a squat.
    Args:
        knee_angle (float): Angle at the knee joint.
        min_depth (float): Minimum acceptable knee angle.
    Returns:
        str: Feedback message.
    """
    if knee_angle > min_depth:
        return "Not deep enough"
    return "Good squat depth"

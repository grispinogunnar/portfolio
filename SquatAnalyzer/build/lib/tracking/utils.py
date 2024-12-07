import cv2

def draw_path(frame, bbox, path):
    """
    Draws the bounding box, center point, and path of the tracked object on the given frame.

    Args:
        frame (numpy.ndarray): The video frame where the bounding box, center point, and path will be drawn.
        bbox (tuple): The bounding box of the tracked object, specified as (x, y, width, height).
        path (list): A list of (x, y) tuples representing the tracked object's path over time.

    Returns:
        numpy.ndarray: The modified frame with the bounding box, center point, and path drawn.
    """
    # Draw bounding box
    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Draw center point
    center_x, center_y = x + w // 2, y + h // 2
    cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    # Draw path
    for i in range(1, len(path)):
        cv2.line(frame, path[i - 1], path[i], (255, 0, 0), 2)

    return frame

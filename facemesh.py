import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh
from mediapipe.python.solutions.drawing_utils import DrawingSpec

drawingModule = mp.solutions.drawing_utils
drawing_spec = drawingModule.DrawingSpec(thickness=15, color=(0,0,0))
def get_facemesh(file):
    with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5) as face_mesh:
        image = cv2.imread(file)
        # Convert the BGR image to RGB before processing.
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Print and draw face mesh landmarks on the image.

        annotated_image = image.copy()
        mask = cv2.inRange(annotated_image, (0, 0, 0), (255, 255, 255))
        annotated_image[mask > 0] = (255, 255, 255)
        for face_landmarks in results.multi_face_landmarks:
            print('face_landmarks:', face_landmarks)
            # mp_drawing.draw_landmarks(
            #     image=annotated_image,
            #     landmark_list=face_landmarks,
            #     connections=mp_face_mesh.FACEMESH_TESSELATION,
            #     landmark_drawing_spec=None,
            #     connection_drawing_spec=mp_drawing_styles
            #         .get_default_face_mesh_tesselation_style())
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec = drawing_spec)
            mp_drawing.draw_landmarks(
                image=annotated_image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_IRISES,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_spec)
    return annotated_image

if __name__ == '__main__':
    annotated_image = get_facemesh('ricardo.jpg')
    cv2.imshow("mesh'd", annotated_image)
    cv2.waitKey(0)

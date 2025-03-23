import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
import torch  # Asegúrate de tener PyTorch instalado
import time

# Cargar el modelo YOLOv5 preentrenado para detección de objetos (usando PyTorch)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # Carga el modelo 'yolov5s' desde GitHub
model.eval()  # Modo de inferencia (desactiva el entrenamiento)

# Lista de cámaras
camera_streams = []

# Variable para controlar el estado del reconocimiento
is_recognition_active = False

# Diccionario para almacenar los objetos detectados y su tiempo de visualización
detected_objects = {}

# Lista para guardar las referencias de las imágenes en Tkinter
detected_objects_images = []

# Función para capturar el video de todas las cámaras
def capture_video():
    global is_recognition_active, detected_objects, detected_objects_images
    caps = [cv2.VideoCapture(stream) for stream in camera_streams]

    for cap in caps:
        if not cap.isOpened():
            messagebox.showerror("Error", f"No se pudo conectar a la cámara: {stream}")
            return

    last_detected = None  # Variable para almacenar el último objeto detectado

    while is_recognition_active:
        for i, cap in enumerate(caps):
            ret, frame = cap.read()
            if not ret:
                continue

            # Reducir el tamaño de la imagen para hacer la detección más rápida
            frame_resized = cv2.resize(frame, (640, 480))  # Reducimos la resolución a 640x480
            results = model(frame_resized)  # El modelo YOLOv5 procesa directamente la imagen
            detections = results.xyxy[0].cpu().numpy()  # Coordenadas de detección (x1, y1, x2, y2, clase, probabilidad)

            # Variables para almacenar la descripción del objeto detectado
            descriptions = []

            # Dibujar los recuadros para los objetos detectados
            for det in detections:
                x1, y1, x2, y2, conf, cls = det
                if conf > 0.5 and int(cls) == 0:  # Umbral de confianza y comprobación de clase "person"
                    # Dibujar un recuadro alrededor del objeto detectado
                    cv2.rectangle(frame_resized, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

                    # Añadir la etiqueta de la clase y la probabilidad
                    label = model.names[int(cls)]  # Obtener el nombre de la clase (ej. 'person', 'car', etc.)
                    description = f"{label}: {conf:.2f}"  # Descripción del objeto con probabilidad
                    descriptions.append(description)

                    # Guardar el objeto detectado con su tiempo de detección si es un nuevo objeto
                    if last_detected != description:
                        detected_objects[description] = {
                            'image': frame_resized[int(y1):int(y2), int(x1):int(x2)],
                            'time': time.time()  # Registrar el tiempo de detección
                        }
                        last_detected = description  # Actualizamos el objeto detectado

            # Eliminar objetos que han superado los 10 segundos
            current_time = time.time()
            detected_objects = {key: value for key, value in detected_objects.items() if current_time - value['time'] < 10}

            # Convertir la imagen de BGR (OpenCV) a RGB (Tkinter)
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(frame_pil)

            # Mostrar la imagen de cada cámara en el canvas correspondiente
            canvas_cam = camera_canvases[i]
            canvas_cam.create_image(0, 0, anchor=tk.NW, image=frame_tk)
            canvas_cam.image = frame_tk

            # Limpiar el canvas de objetos detectados
            detected_objects_canvas.delete("all")
            detected_objects_images = []  # Limpiar la lista de referencias de imágenes

            # Mostrar las imágenes de los objetos detectados en el carril
            y_offset = 10
            for description, obj_data in detected_objects.items():
                obj_image_resized = cv2.resize(obj_data['image'], (180, 100))  # Redimensionar a 180x100
                obj_image_rgb = cv2.cvtColor(obj_image_resized, cv2.COLOR_BGR2RGB)
                obj_image_pil = Image.fromarray(obj_image_rgb)
                obj_image_tk = ImageTk.PhotoImage(obj_image_pil)

                # Mostrar la imagen en el canvas de objetos detectados
                detected_objects_canvas.create_image(10, y_offset, anchor=tk.NW, image=obj_image_tk)
                detected_objects_images.append(obj_image_tk)  # Mantener una referencia de la imagen

                # Mostrar la descripción del objeto
                detected_objects_canvas.create_text(10, y_offset + 110, anchor=tk.NW, text=description, font=("Helvetica", 8), fill="white")

                y_offset += 120  # Aumentar el offset para el siguiente objeto

            # Mostrar la descripción de los objetos detectados
            if descriptions:
                label_description.config(text=f"Objetos Detectados: {', '.join(descriptions)}")
            else:
                label_description.config(text="Objetos Detectados: Ninguno")

            # Actualizar la ventana de Tkinter
            root.update()

    for cap in caps:
        cap.release()

# Función para iniciar o detener el reconocimiento
def toggle_recognition():
    global is_recognition_active
    if is_recognition_active:
        is_recognition_active = False
    else:
        is_recognition_active = True
        capture_video()

# Función para agregar una nueva cámara
def add_camera():
    rtsp_url = askstring("Agregar Cámara", "Introduce la URL RTSP de la cámara:")
    if rtsp_url:
        camera_streams.append(rtsp_url)
        update_canvas_size()

# Función para eliminar una cámara
def remove_camera():
    rtsp_url = askstring("Eliminar Cámara", "Introduce la URL RTSP de la cámara a eliminar:")
    if rtsp_url in camera_streams:
        camera_streams.remove(rtsp_url)
        update_canvas_size()

# Función para actualizar el tamaño del canvas según el número de cámaras
def update_canvas_size():
    global camera_canvases
    for canvas in camera_canvases:
        canvas.destroy()  # Eliminar los canvas actuales

    num_cameras = len(camera_streams)
    camera_canvases = []

    for i in range(num_cameras):
        canvas_cam = tk.Canvas(root, width=320, height=240, bg="black")
        canvas_cam.grid(row=1, column=i, padx=5, pady=5)
        camera_canvases.append(canvas_cam)

# Función para salir de la aplicación
def exit_application():
    global is_recognition_active
    is_recognition_active = False  # Detener el reconocimiento si está activo
    root.quit()  # Cerrar la aplicación

# Configuración de la ventana de Tkinter
root = tk.Tk()
root.title("Reconocimiento de Objetos con XVR Dahua")
root.geometry("1000x600")  # Tamaño inicial de la ventana
root.resizable(True, True)  # Permitir redimensionar la ventana
root.configure(bg="#2E2E2E")  # Fondo de la ventana

# Menu principal
menu = tk.Menu(root)
root.config(menu=menu)

# Submenu para reconocimiento facial
menu.add_command(label="Iniciar/Detener Reconocimiento", command=toggle_recognition)

# Submenu para administrar cámaras
camera_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Administrar Cámaras", menu=camera_menu)
camera_menu.add_command(label="Agregar Cámara", command=add_camera)
camera_menu.add_command(label="Eliminar Cámara", command=remove_camera)

# Submenu para salir
menu.add_command(label="Salir", command=exit_application)

# Frame para la disposición de las cámaras
frame_cameras = tk.Frame(root, bg="#2E2E2E")
frame_cameras.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

# Inicializar la lista de canvas para las cámaras
camera_canvases = []

# Frame para el carril de imágenes de objetos detectados
frame_detected_objects = tk.Frame(root, bg="#2E2E2E")
frame_detected_objects.grid(row=2, column=0, columnspan=3, padx=20, pady=20)

# Canvas para el carril de imágenes de objetos detectados
detected_objects_canvas = tk.Canvas(frame_detected_objects, width=220, height=480, bg="#1C1C1C")
detected_objects_canvas.pack(side=tk.LEFT)

# Etiqueta para mostrar la descripción del objeto detectado
label_description = tk.Label(frame_detected_objects, text="Objetos Detectados:", font=("Helvetica", 12), bg="#2E2E2E", fg="white", anchor='w', width=30)
label_description.pack(side=tk.RIGHT, pady=10)

# Iniciar la interfaz de Tkinter
root.mainloop()
import streamlit as st
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(page_title="SimuColorMix", layout="centered")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("🎨 SimuColorMix")
st.subheader("IoT-based Real-Time Color Recognition & RGB Mixing Simulator")

st.markdown("""
Upload an image, select pixel coordinates,  
extract RGB values and simulate virtual pump mixing.
""")

# ---------------------------------------------------
# IMAGE UPLOAD
# ---------------------------------------------------
uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:

    # Open image using PIL (RGB format)
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Convert PIL Image to NumPy array (RGB)
    img_array = np.array(image)

    height, width, _ = img_array.shape

    # ---------------------------------------------------
    # PIXEL SELECTION
    # ---------------------------------------------------
    st.subheader("Select Pixel Coordinates")

    x = st.number_input(
        "X Coordinate (Width)",
        min_value=0,
        max_value=width - 1,
        value=min(50, width - 1)
    )

    y = st.number_input(
        "Y Coordinate (Height)",
        min_value=0,
        max_value=height - 1,
        value=min(50, height - 1)
    )

    # Extract RGB directly (NO BGR confusion)
    r, g, b = img_array[int(y), int(x)]

    st.write(f"### Extracted Color (R, G, B): ({r}, {g}, {b})")

    # ---------------------------------------------------
    # COLOR PREVIEW
    # ---------------------------------------------------
    st.markdown("### Selected Color Preview")
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    st.color_picker("Extracted Color", hex_color)

    # ---------------------------------------------------
    # PUMP SIMULATION
    # ---------------------------------------------------
    total = r + g + b
    if total == 0:
        total = 1  # Avoid division by zero

    r_perc = (r / total) * 100
    g_perc = (g / total) * 100
    b_perc = (b / total) * 100

    st.markdown("### Pump Simulation (RGB Proportions)")
    st.write(f"🔴 Red Pump: {r_perc:.2f}%")
    st.write(f"🟢 Green Pump: {g_perc:.2f}%")
    st.write(f"🔵 Blue Pump: {b_perc:.2f}%")

    # ---------------------------------------------------
    # BAR GRAPH
    # ---------------------------------------------------
    fig, ax = plt.subplots()

    pumps = ['Red', 'Green', 'Blue']
    values = [r_perc, g_perc, b_perc]

    ax.bar(pumps, values, color=['red', 'green', 'blue'])
    ax.set_ylim(0, 100)
    ax.set_ylabel("Pump Strength (%)")
    ax.set_title("RGB Pump Contribution")

    st.pyplot(fig)

    # ---------------------------------------------------
    # FINAL MIXED COLOR OUTPUT
    # ---------------------------------------------------
    st.markdown("### Final Mixed Color Output")

    final_color = np.zeros((150, 150, 3), dtype=np.uint8)
    final_color[:] = (r, g, b)  # Pure RGB (Correct for Streamlit)

    st.image(final_color, caption="Mixed Output Color", use_container_width=False)

else:
    st.info("Please upload an image to begin.")
# 🌱 Digital Crop Disease Management Portal

A web-based **Crop Disease Management Portal** developed using **Python, Flask, SQLite, HTML, CSS and JavaScript**.

The application helps users identify possible crop diseases based on the **selected crop and observed symptoms**. It also provides crop information, disease information, treatments, prevention methods and disease-record management.

---

## 📌 Project Overview

Farmers and agricultural users may find it difficult to identify crop diseases from visible symptoms.

This project provides a simple web interface where the user can:

1. Select a crop.
2. View symptoms relevant to that crop.
3. Select the symptoms observed in the plant.
4. Search for possible diseases.
5. View disease causes, symptoms, treatment and prevention.
6. View detailed information about different crops.
7. Record disease occurrences.
8. View previously recorded disease cases.

The system currently supports:

- 🌾 Rice
- 🌾 Wheat
- 🍅 Tomato
- 🌽 Maize
- 🥔 Potato

---

# ✨ Features

## 🌱 Crop Selection

Users can select a crop from the available crops.

The current crops are:

- Rice
- Wheat
- Tomato
- Maize
- Potato

Each crop has detailed information such as:

- Scientific name
- Description
- Climate
- Temperature
- Rainfall
- Soil type
- Soil pH
- Growing season
- Sowing time
- Harvesting time
- Recommended fertilizer
- Uses
- Disease prevention

---

# 🔍 Crop-Based Disease Search

The disease search is based on both:

**Crop + Symptoms**

The application does not require users to search through every symptom in the database.

After selecting a crop, only symptoms relevant to that crop should be presented to the user.

### Example
Reference searches
Crop	----->Main Symptoms
🌾 Rice	--> Brown lesions, diamond-shaped lesions, brown spots, yellowing
🌾 Wheat-->	 Orange pustules, yellowing, white powder
🍅 Tomato--> Leaf spots, water-soaked lesions, fruit lesions, leaf curling
🌽 Maize-->	 Long lesions, leaf spots, reddish-brown pustules
🥔 Potato-->	Brown spots, water-soaked lesions, tuber lesions, wilting

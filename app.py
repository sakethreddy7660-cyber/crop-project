import sqlite3
from flask import Flask, render_template, request, jsonify
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


# =====================================================
# DATABASE
# =====================================================

def get_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()

    conn.executescript("""
    
    CREATE TABLE IF NOT EXISTS crops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        scientific_name TEXT,
        climate TEXT,
        temperature TEXT,
        rainfall TEXT,
        soil TEXT,
        soil_ph TEXT,
        season TEXT,
        sowing_time TEXT,
        harvesting_time TEXT,
        fertilizer TEXT,
        uses TEXT,
        prevention TEXT
    );

    CREATE TABLE IF NOT EXISTS diseases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        crop_id INTEGER,
        name TEXT,
        symptoms TEXT,
        cause TEXT,
        treatment TEXT,
        prevention TEXT,
        severity TEXT
    );

    CREATE TABLE IF NOT EXISTS symptoms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE
    );

    CREATE TABLE IF NOT EXISTS disease_symptoms (
        disease_id INTEGER,
        symptom_id INTEGER,
        PRIMARY KEY (disease_id, symptom_id)
    );

    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farmer TEXT,
        crop_id INTEGER,
        disease_id INTEGER,
        area REAL,
        date TEXT,
        severity TEXT,
        notes TEXT
    );

    """)

    # -------------------------------------------------
    # CROPS
    # -------------------------------------------------

    crops = [
        (
            "Rice",
            "An important cereal crop grown mainly in warm and humid conditions.",
            "Oryza sativa",
            "Warm and humid",
            "20-35°C",
            "1000-2000 mm",
            "Clay or loamy soil",
            "5.5-6.5",
            "Kharif",
            "June-July",
            "October-November",
            "NPK fertilizer and organic manure",
            "Food, flour and animal feed",
            "Use healthy seed, proper irrigation and balanced fertilizer"
        ),
        (
            "Wheat",
            "An important winter cereal crop.",
            "Triticum aestivum",
            "Cool and dry",
            "10-25°C",
            "450-650 mm",
            "Loamy soil",
            "6.0-7.5",
            "Rabi",
            "October-November",
            "March-April",
            "NPK fertilizer and nitrogen",
            "Flour, bread and animal feed",
            "Use resistant varieties and healthy seed"
        ),
        (
            "Tomato",
            "An important vegetable crop grown in many regions.",
            "Solanum lycopersicum",
            "Warm",
            "18-30°C",
            "600-1200 mm",
            "Loamy soil",
            "6.0-7.0",
            "Kharif/Rabi",
            "June-July or September-October",
            "September-November or January-March",
            "NPK fertilizer and organic manure",
            "Vegetables, sauces and juice",
            "Use healthy seedlings and maintain good field hygiene"
        ),
        (
            "Maize",
            "An important cereal crop used for food and animal feed.",
            "Zea mays",
            "Warm",
            "18-27°C",
            "500-800 mm",
            "Well-drained loamy soil",
            "5.5-7.0",
            "Kharif/Rabi",
            "June-July",
            "September-October",
            "NPK fertilizer and nitrogen",
            "Food, animal feed and industrial products",
            "Use healthy seed, crop rotation and proper irrigation"
        ),
        (
            "Potato",
            "An important tuber crop grown mainly during cool weather.",
            "Solanum tuberosum",
            "Cool",
            "15-20°C",
            "500-700 mm",
            "Sandy loam soil",
            "5.0-6.5",
            "Rabi",
            "October-November",
            "January-February",
            "NPK fertilizer and organic manure",
            "Food, chips and starch",
            "Use certified seed, good drainage and crop rotation"
        )
    ]

    for crop in crops:
        conn.execute("""
            INSERT OR IGNORE INTO crops
            (name, description, scientific_name, climate, temperature,
             rainfall, soil, soil_ph, season, sowing_time,
             harvesting_time, fertilizer, uses, prevention)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, crop)


    # -------------------------------------------------
    # SYMPTOMS
    # -------------------------------------------------

    symptoms = [
        "Brown lesions",
        "Diamond-shaped lesions",
        "Brown spots",
        "Yellowing leaves",
        "Orange pustules",
        "White powder on leaves",
        "Dark leaf spots",
        "Water-soaked lesions",
        "Fruit lesions",
        "Leaf curling",
        "Stunted growth",
        "Long gray-green lesions",
        "Leaf spots",
        "Reddish-brown pustules",
        "Concentric leaf spots",
        "Tuber lesions",
        "Plant wilting"
    ]

    for symptom in symptoms:
        conn.execute(
            "INSERT OR IGNORE INTO symptoms (name) VALUES (?)",
            (symptom,)
        )


    # -------------------------------------------------
    # DISEASES
    # -------------------------------------------------

    diseases = [

        # Rice
        (
            "Rice",
            "Blast",
            "Brown lesions, diamond-shaped lesions, yellowing leaves",
            "Fungus",
            "Use recommended fungicides and follow agricultural guidance.",
            "Use resistant varieties, healthy seed and balanced fertilizer.",
            "High"
        ),
        (
            "Rice",
            "Brown Spot",
            "Brown spots, yellowing leaves",
            "Fungus",
            "Use recommended fungicides and maintain proper nutrition.",
            "Use clean seed and balanced fertilizer.",
            "Moderate"
        ),

        # Wheat
        (
            "Wheat",
            "Wheat Rust",
            "Orange pustules, yellowing leaves",
            "Fungus",
            "Use recommended fungicides.",
            "Use resistant varieties and healthy seed.",
            "High"
        ),
        (
            "Wheat",
            "Powdery Mildew",
            "White powder on leaves, yellowing leaves",
            "Fungus",
            "Use recommended fungicides.",
            "Use resistant varieties and good field ventilation.",
            "Moderate"
        ),

        # Tomato
        (
            "Tomato",
            "Early Blight",
            "Dark leaf spots, yellowing leaves",
            "Fungus",
            "Use recommended fungicides and remove severely infected leaves.",
            "Use healthy seedlings and maintain field hygiene.",
            "Moderate"
        ),
        (
            "Tomato",
            "Late Blight",
            "Water-soaked lesions, dark leaf spots, fruit lesions",
            "Fungus-like pathogen",
            "Use recommended fungicides and remove infected plant material.",
            "Maintain good drainage and air circulation.",
            "High"
        ),
        (
            "Tomato",
            "Tomato Leaf Curl",
            "Leaf curling, yellowing leaves, stunted growth",
            "Virus",
            "Control insect vectors and remove severely infected plants.",
            "Use healthy seedlings and control whiteflies.",
            "High"
        ),

        # Maize
        (
            "Maize",
            "Northern Corn Leaf Blight",
            "Long gray-green lesions, leaf spots",
            "Fungus",
            "Use recommended fungicides.",
            "Use resistant hybrids and healthy seed.",
            "Moderate"
        ),
        (
            "Maize",
            "Common Rust",
            "Reddish-brown pustules, yellowing leaves",
            "Fungus",
            "Use recommended fungicides.",
            "Use resistant varieties.",
            "Moderate"
        ),

        # Potato
        (
            "Potato",
            "Potato Early Blight",
            "Brown spots, concentric leaf spots",
            "Fungus",
            "Use recommended fungicides.",
            "Use healthy seed and proper crop rotation.",
            "Moderate"
        ),
        (
            "Potato",
            "Potato Late Blight",
            "Water-soaked lesions, dark leaf spots, tuber lesions",
            "Fungus-like pathogen",
            "Use recommended fungicides and remove infected plant material.",
            "Use healthy seed and maintain good drainage.",
            "High"
        ),
        (
            "Potato",
            "Potato Bacterial Wilt",
            "Plant wilting, yellowing leaves, stunted growth",
            "Bacteria",
            "Remove infected plants and follow local agricultural recommendations.",
            "Use certified seed and practice crop rotation.",
            "High"
        )
    ]

    for disease in diseases:

        crop = conn.execute(
            "SELECT id FROM crops WHERE name = ?",
            (disease[0],)
        ).fetchone()

        if crop:

            conn.execute("""
                INSERT OR IGNORE INTO diseases
                (crop_id, name, symptoms, cause, treatment,
                 prevention, severity)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                crop["id"],
                disease[1],
                disease[2],
                disease[3],
                disease[4],
                disease[5],
                disease[6]
            ))


    # -------------------------------------------------
    # CONNECT DISEASES WITH SYMPTOMS
    # -------------------------------------------------

    connections = {
        "Blast": [
            "Brown lesions",
            "Diamond-shaped lesions",
            "Yellowing leaves"
        ],

        "Brown Spot": [
            "Brown spots",
            "Yellowing leaves"
        ],

        "Wheat Rust": [
            "Orange pustules",
            "Yellowing leaves"
        ],

        "Powdery Mildew": [
            "White powder on leaves",
            "Yellowing leaves"
        ],

        "Early Blight": [
            "Dark leaf spots",
            "Yellowing leaves"
        ],

        "Late Blight": [
            "Water-soaked lesions",
            "Dark leaf spots",
            "Fruit lesions"
        ],

        "Tomato Leaf Curl": [
            "Leaf curling",
            "Yellowing leaves",
            "Stunted growth"
        ],

        "Northern Corn Leaf Blight": [
            "Long gray-green lesions",
            "Leaf spots"
        ],

        "Common Rust": [
            "Reddish-brown pustules",
            "Yellowing leaves"
        ],

        "Potato Early Blight": [
            "Brown spots",
            "Concentric leaf spots"
        ],

        "Potato Late Blight": [
            "Water-soaked lesions",
            "Dark leaf spots",
            "Tuber lesions"
        ],

        "Potato Bacterial Wilt": [
            "Plant wilting",
            "Yellowing leaves",
            "Stunted growth"
        ]
    }

    for disease_name, symptom_list in connections.items():

        disease = conn.execute(
            "SELECT id FROM diseases WHERE name = ?",
            (disease_name,)
        ).fetchone()

        if disease:

            for symptom_name in symptom_list:

                symptom = conn.execute(
                    "SELECT id FROM symptoms WHERE name = ?",
                    (symptom_name,)
                ).fetchone()

                if symptom:

                    conn.execute("""
                        INSERT OR IGNORE INTO disease_symptoms
                        (disease_id, symptom_id)
                        VALUES (?, ?)
                    """, (
                        disease["id"],
                        symptom["id"]
                    ))

    conn.commit()
    conn.close()

    print("Database initialized successfully!")


# =====================================================
# HOME
# =====================================================

@app.route("/")
def index():

    conn = get_db()

    crops = conn.execute("""
        SELECT id, name
        FROM crops
        ORDER BY name
    """).fetchall()

    conn.close()

    return render_template(
        "index.html",
        crops=crops
    )


# =====================================================
# SEARCH DISEASES
# =====================================================

@app.route("/search", methods=["GET", "POST"])
def search():

    conn = get_db()

    crops = conn.execute("""
        SELECT id, name
        FROM crops
        ORDER BY name
    """).fetchall()

    symptoms = conn.execute("""
        SELECT id, name
        FROM symptoms
        ORDER BY name
    """).fetchall()

    diseases = []
    search_performed = False

    if request.method == "POST":

        crop_id = request.form.get("crop_id")
        symptom_ids = request.form.getlist("symptoms")

        search_performed = True

        if crop_id and symptom_ids:

            placeholders = ",".join(
                "?" for _ in symptom_ids
            )

            query = f"""
                SELECT DISTINCT
                    d.id,
                    d.name,
                    d.symptoms,
                    d.cause,
                    d.treatment,
                    d.prevention,
                    d.severity
                FROM diseases d
                JOIN disease_symptoms ds
                    ON d.id = ds.disease_id
                WHERE d.crop_id = ?
                AND ds.symptom_id IN ({placeholders})
            """

            diseases = conn.execute(
                query,
                [crop_id] + symptom_ids
            ).fetchall()

    conn.close()

    return render_template(
        "search.html",
        crops=crops,
        symptoms=symptoms,
        diseases=diseases,
        search_performed=search_performed
    )


# =====================================================
# DISEASE DETAILS
# =====================================================

@app.route("/disease/<int:disease_id>")
def disease_detail(disease_id):

    conn = get_db()

    disease = conn.execute("""
        SELECT
            d.id,
            d.name,
            d.symptoms,
            d.cause,
            d.treatment,
            d.prevention,
            d.severity,
            c.name AS crop_name
        FROM diseases d
        JOIN crops c
            ON d.crop_id = c.id
        WHERE d.id = ?
    """, (disease_id,)).fetchone()

    symptoms = conn.execute("""
        SELECT s.name
        FROM symptoms s
        JOIN disease_symptoms ds
            ON s.id = ds.symptom_id
        WHERE ds.disease_id = ?
    """, (disease_id,)).fetchall()

    conn.close()

    if not disease:
        return "Disease not found", 404

    image_map = {
        "Blast": "blast.jpg",
        "Brown Spot": "brown_spot.jpg",
        "Wheat Rust": "wheat_rust.jpg",
        "Powdery Mildew": "powdery_mildew.jpg",
        "Early Blight": "early_blight.jpg",
        "Late Blight": "late_blight.jpg",
        "Tomato Leaf Curl": "tomato_leaf_curl.jpg",
        "Northern Corn Leaf Blight": "corn_leaf_blight.jpg",
        "Common Rust": "common_rust.jpg",
        "Potato Early Blight": "potato_early_blight.jpg",
        "Potato Late Blight": "potato_late_blight.jpg",
        "Potato Bacterial Wilt": "potato_wilt.jpg"
    }

    image_name = image_map.get(
        disease["name"],
        "default.jpg"
    )

    return render_template(
        "disease_detail.html",
        disease=disease,
        symptoms=symptoms,
        image_name=image_name
    )


# =====================================================
# CROP DETAILS
# =====================================================

@app.route("/crop/<int:crop_id>")
def crop_details(crop_id):

    conn = get_db()

    crop = conn.execute("""
        SELECT
            name,
            description,
            scientific_name,
            climate,
            temperature,
            rainfall,
            soil,
            soil_ph,
            season,
            sowing_time,
            harvesting_time,
            fertilizer,
            uses,
            prevention
        FROM crops
        WHERE id = ?
    """, (crop_id,)).fetchone()

    diseases = conn.execute("""
        SELECT name
        FROM diseases
        WHERE crop_id = ?
        ORDER BY name
    """, (crop_id,)).fetchall()

    conn.close()

    if not crop:
        return "Crop not found", 404

    return render_template(
        "crop_details.html",
        crop=crop,
        diseases=diseases
    )


# =====================================================
# RECORD DISEASE
# =====================================================

@app.route("/record", methods=["GET", "POST"])
def record():

    conn = get_db()

    crops = conn.execute("""
        SELECT id, name
        FROM crops
        ORDER BY name
    """).fetchall()

    diseases = conn.execute("""
        SELECT id, name
        FROM diseases
        ORDER BY name
    """).fetchall()

    message = None

    if request.method == "POST":

        farmer = request.form.get("farmer_name")
        crop_id = request.form.get("crop_id")
        disease_id = request.form.get("disease_id")
        area = request.form.get("affected_area")
        date = request.form.get("date_observed")
        severity = request.form.get("severity")
        notes = request.form.get("notes")

        if farmer and crop_id and disease_id and area and date:

            try:

                conn.execute("""
                    INSERT INTO records
                    (farmer, crop_id, disease_id, area,
                     date, severity, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    farmer,
                    crop_id,
                    disease_id,
                    float(area),
                    date,
                    severity,
                    notes
                ))

                conn.commit()

                message = "Record saved successfully!"

            except Exception as e:

                message = "Error: " + str(e)

        else:

            message = "Please fill all required fields!"

    conn.close()

    return render_template(
        "record.html",
        crops=crops,
        diseases=diseases,
        message=message
    )


# =====================================================
# VIEW RECORDS
# =====================================================

@app.route("/view-records")
def view_records():

    conn = get_db()

    records = conn.execute("""
        SELECT
            r.id,
            r.farmer,
            c.name AS crop_name,
            d.name AS disease_name,
            r.area,
            r.date,
            r.severity,
            r.notes
        FROM records r
        JOIN crops c
            ON r.crop_id = c.id
        JOIN diseases d
            ON r.disease_id = d.id
        ORDER BY r.date DESC
    """).fetchall()

    conn.close()

    return render_template(
        "view_records.html",
        records=records
    )


# =====================================================
# API
# =====================================================

@app.route("/api/diseases/<int:crop_id>")
def get_diseases_by_crop(crop_id):

    conn = get_db()

    diseases = conn.execute("""
        SELECT id, name
        FROM diseases
        WHERE crop_id = ?
        ORDER BY name
    """, (crop_id,)).fetchall()

    conn.close()

    return jsonify([
        {
            "id": disease["id"],
            "name": disease["name"]
        }
        for disease in diseases
    ])


# =====================================================
# ERROR PAGES
# =====================================================

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
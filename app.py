from flask import Flask, request, jsonify, render_template, session
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Compressed class schedules with capacity and timing
classes = {
    "yoga": {
        "name": "Yoga",
        "timings": ["6 AM", "7 AM", "6 PM", "7 PM"],
        "days": ["Monday", "Wednesday", "Friday", "Saturday"],
        "duration": "60 min",
        "difficulty": "Beginner",
        "capacity": 20,
        "enrolled": 12,
        "trainer": "Sarah Johnson"
    },
    "zumba": {
        "name": "Zumba",
        "timings": ["8 AM", "7 PM", "8 PM"],
        "days": ["Tuesday", "Thursday", "Saturday"],
        "duration": "45 min",
        "difficulty": "Intermediate",
        "capacity": 25,
        "enrolled": 18,
        "trainer": "Maria Garcia"
    },
    "cardio": {
        "name": "Cardio Blast",
        "timings": ["6 AM", "5 PM", "6 PM"],
        "days": ["Monday", "Wednesday", "Friday"],
        "duration": "45 min",
        "difficulty": "Advanced",
        "capacity": 15,
        "enrolled": 10,
        "trainer": "Mike Chen"
    },
    "pilates": {
        "name": "Pilates",
        "timings": ["9 AM", "5 PM"],
        "days": ["Tuesday", "Thursday", "Sunday"],
        "duration": "60 min",
        "difficulty": "Beginner",
        "capacity": 15,
        "enrolled": 8,
        "trainer": "Emma Wilson"
    },
    "hiit": {
        "name": "HIIT Training",
        "timings": ["7 AM", "6 PM"],
        "days": ["Monday", "Wednesday", "Friday"],
        "duration": "30 min",
        "difficulty": "Advanced",
        "capacity": 12,
        "enrolled": 11,
        "trainer": "Jake Thompson"
    },
    "spinning": {
        "name": "Spinning",
        "timings": ["6 AM", "7 AM", "7 PM"],
        "days": ["Tuesday", "Thursday", "Saturday"],
        "duration": "45 min",
        "difficulty": "Intermediate",
        "capacity": 20,
        "enrolled": 15,
        "trainer": "Lisa Park"
    }
}

# Trainer profiles with detailed information
trainers = {
    "Sarah Johnson": {
        "name": "Sarah Johnson",
        "specialization": "Yoga & Meditation",
        "experience": "8 years",
        "rating": 4.9,
        "certifications": ["RYT-500", "Meditation Instructor"],
        "bio": "Certified yoga instructor specializing in Hatha and Vinyasa yoga"
    },
    "Maria Garcia": {
        "name": "Maria Garcia",
        "specialization": "Dance Fitness",
        "experience": "6 years",
        "rating": 4.8,
        "certifications": ["Zumba Instructor", "Group Fitness"],
        "bio": "High-energy dance fitness expert with Latin dance background"
    },
    "Mike Chen": {
        "name": "Mike Chen",
        "specialization": "Cardio & Strength",
        "experience": "10 years",
        "rating": 4.9,
        "certifications": ["NASM-CPT", "CrossFit Level 2"],
        "bio": "Former athlete specializing in high-intensity cardio training"
    },
    "Emma Wilson": {
        "name": "Emma Wilson",
        "specialization": "Pilates & Core",
        "experience": "7 years",
        "rating": 4.7,
        "certifications": ["PMA Certified", "Mat Pilates"],
        "bio": "Pilates expert focused on core strength and flexibility"
    },
    "Jake Thompson": {
        "name": "Jake Thompson",
        "specialization": "HIIT & Functional Training",
        "experience": "5 years",
        "rating": 4.8,
        "certifications": ["HIIT Specialist", "TRX Instructor"],
        "bio": "Intense HIIT trainer helping clients achieve maximum results"
    },
    "Lisa Park": {
        "name": "Lisa Park",
        "specialization": "Cycling & Endurance",
        "experience": "9 years",
        "rating": 4.9,
        "certifications": ["Spinning Instructor", "Endurance Coach"],
        "bio": "Professional cyclist turned spinning instructor"
    }
}

# Membership tiers with benefits
membership_tiers = {
    "basic": {
        "name": "Basic",
        "monthly_bookings": 5,
        "priority_booking": False,
        "personal_trainer": False,
        "exclusive_classes": False,
        "price": "$29/month"
    },
    "premium": {
        "name": "Premium",
        "monthly_bookings": 15,
        "priority_booking": True,
        "personal_trainer": False,
        "exclusive_classes": False,
        "price": "$59/month"
    },
    "vip": {
        "name": "VIP",
        "monthly_bookings": -1,  # Unlimited
        "priority_booking": True,
        "personal_trainer": True,
        "exclusive_classes": True,
        "price": "$99/month"
    }
}

# Simulated user data (in production, this would be a database)
users = {
    "demo_user": {
        "name": "Alex",
        "membership": "premium",
        "bookings": [],
        "bookings_this_month": 3
    }
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    # Initialize session
    if 'user_id' not in session:
        session['user_id'] = 'demo_user'
    if 'selected_class' not in session:
        session['selected_class'] = ''
    
    user_msg = request.json["message"].lower().strip()
    user_id = session['user_id']
    user = users.get(user_id, users["demo_user"])
    
    # Greeting
    if any(word in user_msg for word in ["hi", "hello", "hey", "start"]):
        class_list = ", ".join([c["name"] for c in classes.values()])
        return jsonify(reply=f"Hello {user.get('name', 'there')}! 👋 Welcome to FitLife Gym 💪\n\nAvailable classes: {class_list}\n\nYou can also ask about trainers, membership, or booking history!")
    
    # Membership info
    if "membership" in user_msg or "tier" in user_msg or "plan" in user_msg:
        tier = membership_tiers[user["membership"]]
        bookings_left = tier["monthly_bookings"] - user["bookings_this_month"] if tier["monthly_bookings"] != -1 else "Unlimited"
        return jsonify(reply=f"📋 Your Membership: {tier['name']} ({tier['price']})\n\n✅ Benefits:\n• Bookings: {bookings_left} remaining this month\n• Priority Booking: {'Yes' if tier['priority_booking'] else 'No'}\n• Personal Trainer: {'Yes' if tier['personal_trainer'] else 'No'}\n• Exclusive Classes: {'Yes' if tier['exclusive_classes'] else 'No'}")
    
    # Trainer info
    if "trainer" in user_msg:
        if any(name.lower() in user_msg for name in trainers.keys()):
            # Specific trainer
            for name, info in trainers.items():
                if name.lower() in user_msg:
                    return jsonify(reply=f"👨‍🏫 {info['name']}\n\n⭐ Rating: {info['rating']}/5.0\n🎯 Specialization: {info['specialization']}\n📅 Experience: {info['experience']}\n🏆 Certifications: {', '.join(info['certifications'])}\n\n{info['bio']}")
        else:
            # List all trainers
            trainer_list = "\n\n".join([f"• {t['name']} - {t['specialization']} (⭐ {t['rating']})" for t in trainers.values()])
            return jsonify(reply=f"👥 Our Expert Trainers:\n\n{trainer_list}\n\nAsk about a specific trainer for more details!")
    
    # Booking history
    if "history" in user_msg or "my booking" in user_msg or "booked" in user_msg:
        if user["bookings"]:
            booking_list = "\n".join([f"• {b['class']} - {b['time']} on {b['day']}" for b in user["bookings"]])
            return jsonify(reply=f"📅 Your Bookings:\n\n{booking_list}\n\nTo cancel, type 'cancel [class name]'")
        else:
            return jsonify(reply="You have no bookings yet. Book a class to get started!")
    
    # Cancel booking
    if "cancel" in user_msg:
        for class_key in classes.keys():
            if class_key in user_msg:
                user["bookings"] = [b for b in user["bookings"] if class_key not in b["class"].lower()]
                user["bookings_this_month"] = max(0, user["bookings_this_month"] - 1)
                classes[class_key]["enrolled"] = max(0, classes[class_key]["enrolled"] - 1)
                session['selected_class'] = ''
                return jsonify(reply=f"❌ Your {classes[class_key]['name']} booking has been cancelled.")
        return jsonify(reply="Please specify which class to cancel (e.g., 'cancel yoga')")
    
    # Class selection
    if user_msg in classes:
        class_info = classes[user_msg]
        session['selected_class'] = user_msg
        trainer_info = trainers[class_info["trainer"]]
        available_spots = class_info["capacity"] - class_info["enrolled"]
        
        return jsonify(reply=f"🏋️ {class_info['name']}\n\n⏰ Timings: {', '.join(class_info['timings'])}\n📅 Days: {', '.join(class_info['days'])}\n⏱️ Duration: {class_info['duration']}\n📊 Difficulty: {class_info['difficulty']}\n👥 Available Spots: {available_spots}/{class_info['capacity']}\n👨‍🏫 Trainer: {class_info['trainer']} (⭐ {trainer_info['rating']})\n\nChoose a time to book!")
    
    # Time selection for booking
    if session.get('selected_class') and any(time in user_msg for time in ["am", "pm"]):
        class_key = session['selected_class']
        class_info = classes[class_key]
        
        # Check capacity
        if class_info["enrolled"] >= class_info["capacity"]:
            return jsonify(reply=f"❌ Sorry, {class_info['name']} is fully booked! Try another time or class.")
        
        # Check membership limits
        tier = membership_tiers[user["membership"]]
        if tier["monthly_bookings"] != -1 and user["bookings_this_month"] >= tier["monthly_bookings"]:
            return jsonify(reply=f"❌ You've reached your monthly booking limit ({tier['monthly_bookings']} bookings). Upgrade to Premium or VIP for more!")
        
        # Book the class
        booking = {
            "class": class_info["name"],
            "time": user_msg.upper(),
            "day": class_info["days"][0],
            "trainer": class_info["trainer"]
        }
        user["bookings"].append(booking)
        user["bookings_this_month"] += 1
        class_info["enrolled"] += 1
        
        session['selected_class'] = ''
        return jsonify(reply=f"✅ Booking Confirmed!\n\n🏋️ Class: {class_info['name']}\n⏰ Time: {user_msg.upper()}\n📅 Day: {booking['day']}\n👨‍🏫 Trainer: {class_info['trainer']}\n\nSee you there! 💪")
    
    # Help/default
    return jsonify(reply="I can help you with:\n• View classes (yoga, zumba, cardio, pilates, hiit, spinning)\n• Check trainers\n• View membership info\n• See booking history\n• Book or cancel classes\n\nWhat would you like to do?")

if __name__ == "__main__":
    app.run(debug=True)
"""
Comprehensive City Directory & Coordinate Geocoding Service.
Provides latitude, longitude, and timezone offsets for major Indian and global cities.
"""
from typing import Dict, Tuple, Optional


CITY_DATABASE = {
    # Karnataka
    "bengaluru": (12.9716, 77.5946, 5.5, "Bengaluru, Karnataka, India"),
    "bangalore": (12.9716, 77.5946, 5.5, "Bengaluru, Karnataka, India"),
    "mysuru": (12.2958, 76.6394, 5.5, "Mysuru, Karnataka, India"),
    "mysore": (12.2958, 76.6394, 5.5, "Mysuru, Karnataka, India"),
    "hubballi": (15.3647, 75.1240, 5.5, "Hubballi, Karnataka, India"),
    "hubli": (15.3647, 75.1240, 5.5, "Hubballi, Karnataka, India"),
    "mangaluru": (12.9141, 74.8560, 5.5, "Mangaluru, Karnataka, India"),
    "mangalore": (12.9141, 74.8560, 5.5, "Mangaluru, Karnataka, India"),
    "belagavi": (15.8497, 74.4977, 5.5, "Belagavi, Karnataka, India"),
    "belgaum": (15.8497, 74.4977, 5.5, "Belagavi, Karnataka, India"),
    "kalaburagi": (17.3297, 76.8343, 5.5, "Kalaburagi, Karnataka, India"),
    "gulbarga": (17.3297, 76.8343, 5.5, "Kalaburagi, Karnataka, India"),
    "dharwad": (15.4589, 75.0078, 5.5, "Dharwad, Karnataka, India"),
    "shivamogga": (13.9299, 75.5681, 5.5, "Shivamogga, Karnataka, India"),
    "shimoga": (13.9299, 75.5681, 5.5, "Shivamogga, Karnataka, India"),
    "davangere": (14.4644, 75.9218, 5.5, "Davangere, Karnataka, India"),
    "ballari": (15.1394, 76.9214, 5.5, "Ballari, Karnataka, India"),
    "bellary": (15.1394, 76.9214, 5.5, "Ballari, Karnataka, India"),
    "tumakuru": (13.3392, 77.1015, 5.5, "Tumakuru, Karnataka, India"),
    "tumkur": (13.3392, 77.1015, 5.5, "Tumakuru, Karnataka, India"),
    "hassan": (13.0072, 76.0963, 5.5, "Hassan, Karnataka, India"),
    "mandya": (12.5224, 76.8967, 5.5, "Mandya, Karnataka, India"),
    "udupi": (13.3409, 74.7421, 5.5, "Udupi, Karnataka, India"),

    # Tamil Nadu
    "chennai": (13.0827, 80.2707, 5.5, "Chennai, Tamil Nadu, India"),
    "madras": (13.0827, 80.2707, 5.5, "Chennai, Tamil Nadu, India"),
    "coimbatore": (11.0168, 76.9558, 5.5, "Coimbatore, Tamil Nadu, India"),
    "madurai": (9.9252, 78.1198, 5.5, "Madurai, Tamil Nadu, India"),
    "tiruchirappalli": (10.7905, 78.7047, 5.5, "Tiruchirappalli, Tamil Nadu, India"),
    "trichy": (10.7905, 78.7047, 5.5, "Tiruchirappalli, Tamil Nadu, India"),
    "salem": (11.6643, 78.1460, 5.5, "Salem, Tamil Nadu, India"),
    "tirunelveli": (8.7139, 77.7567, 5.5, "Tirunelveli, Tamil Nadu, India"),

    # Telangana & Andhra Pradesh
    "hyderabad": (17.3850, 78.4867, 5.5, "Hyderabad, Telangana, India"),
    "secunderabad": (17.4399, 78.4983, 5.5, "Secunderabad, Telangana, India"),
    "warangal": (17.9689, 79.5941, 5.5, "Warangal, Telangana, India"),
    "vijayawada": (16.5062, 80.6480, 5.5, "Vijayawada, Andhra Pradesh, India"),
    "visakhapatnam": (17.6868, 83.2185, 5.5, "Visakhapatnam, Andhra Pradesh, India"),
    "vizag": (17.6868, 83.2185, 5.5, "Visakhapatnam, Andhra Pradesh, India"),
    "tirupati": (13.6288, 79.4192, 5.5, "Tirupati, Andhra Pradesh, India"),
    "guntur": (16.3067, 80.4365, 5.5, "Guntur, Andhra Pradesh, India"),
    "chittoor": (13.2172, 79.1003, 5.5, "Chittoor, Andhra Pradesh, India"),

    # Maharashtra
    "mumbai": (19.0760, 72.8777, 5.5, "Mumbai, Maharashtra, India"),
    "bombay": (19.0760, 72.8777, 5.5, "Mumbai, Maharashtra, India"),
    "pune": (18.5204, 73.8567, 5.5, "Pune, Maharashtra, India"),
    "nagpur": (21.1458, 79.0882, 5.5, "Nagpur, Maharashtra, India"),
    "nashik": (19.9975, 73.7898, 5.5, "Nashik, Maharashtra, India"),
    "aurangabad": (19.8762, 75.3433, 5.5, "Chhatrapati Sambhajinagar, Maharashtra, India"),
    "chhatrapati sambhajinagar": (19.8762, 75.3433, 5.5, "Chhatrapati Sambhajinagar, Maharashtra, India"),
    "solapur": (17.6599, 75.9064, 5.5, "Solapur, Maharashtra, India"),
    "kolhapur": (16.7050, 74.2433, 5.5, "Kolhapur, Maharashtra, India"),

    # Delhi & NCR
    "delhi": (28.6139, 77.2090, 5.5, "New Delhi, Delhi, India"),
    "new delhi": (28.6139, 77.2090, 5.5, "New Delhi, Delhi, India"),
    "noida": (28.5355, 77.3910, 5.5, "Noida, Uttar Pradesh, India"),
    "gurugram": (28.4595, 77.0266, 5.5, "Gurugram, Haryana, India"),
    "gurgaon": (28.4595, 77.0266, 5.5, "Gurugram, Haryana, India"),
    "faridabad": (28.4089, 77.3178, 5.5, "Faridabad, Haryana, India"),
    "ghaziabad": (28.6692, 77.4538, 5.5, "Ghaziabad, Uttar Pradesh, India"),

    # Northern & Central India
    "jaipur": (26.9124, 75.7873, 5.5, "Jaipur, Rajasthan, India"),
    "jodhpur": (26.2389, 73.0243, 5.5, "Jodhpur, Rajasthan, India"),
    "udaipur": (24.5854, 73.7125, 5.5, "Udaipur, Rajasthan, India"),
    "lucknow": (26.8467, 80.9462, 5.5, "Lucknow, Uttar Pradesh, India"),
    "kanpur": (26.4499, 80.3319, 5.5, "Kanpur, Uttar Pradesh, India"),
    "varanasi": (25.3176, 82.9739, 5.5, "Varanasi, Uttar Pradesh, India"),
    "kashi": (25.3176, 82.9739, 5.5, "Varanasi, Uttar Pradesh, India"),
    "banaras": (25.3176, 82.9739, 5.5, "Varanasi, Uttar Pradesh, India"),
    "prayagraj": (25.4358, 81.8463, 5.5, "Prayagraj, Uttar Pradesh, India"),
    "allahabad": (25.4358, 81.8463, 5.5, "Prayagraj, Uttar Pradesh, India"),
    "agra": (27.1767, 78.0081, 5.5, "Agra, Uttar Pradesh, India"),
    "chandigarh": (30.7333, 76.7794, 5.5, "Chandigarh, India"),
    "amritsar": (31.6340, 74.8723, 5.5, "Amritsar, Punjab, India"),
    "ludhiana": (30.9010, 75.8573, 5.5, "Ludhiana, Punjab, India"),
    "bhopal": (23.2599, 77.4126, 5.5, "Bhopal, Madhya Pradesh, India"),
    "indore": (22.7196, 75.8577, 5.5, "Indore, Madhya Pradesh, India"),
    "gwalior": (26.2183, 78.1828, 5.5, "Gwalior, Madhya Pradesh, India"),
    "jabalpur": (23.1815, 79.9864, 5.5, "Jabalpur, Madhya Pradesh, India"),

    # Eastern India
    "kolkata": (22.5726, 88.3639, 5.5, "Kolkata, West Bengal, India"),
    "calcutta": (22.5726, 88.3639, 5.5, "Kolkata, West Bengal, India"),
    "howrah": (22.5958, 88.2636, 5.5, "Howrah, West Bengal, India"),
    "patna": (25.5941, 85.1376, 5.5, "Patna, Bihar, India"),
    "gaya": (24.7914, 85.0002, 5.5, "Gaya, Bihar, India"),
    "bhubaneswar": (20.2961, 85.8245, 5.5, "Bhubaneswar, Odisha, India"),
    "cuttack": (20.4625, 85.8828, 5.5, "Cuttack, Odisha, India"),
    "ranchi": (23.3441, 85.3096, 5.5, "Ranchi, Jharkhand, India"),
    "jamshedpur": (22.8046, 86.2029, 5.5, "Jamshedpur, Jharkhand, India"),
    "guwahati": (26.1445, 91.7362, 5.5, "Guwahati, Assam, India"),

    # Western India
    "ahmedabad": (23.0225, 72.5714, 5.5, "Ahmedabad, Gujarat, India"),
    "surat": (21.1702, 72.8311, 5.5, "Surat, Gujarat, India"),
    "vadodara": (22.3072, 73.1812, 5.5, "Vadodara, Gujarat, India"),
    "baroda": (22.3072, 73.1812, 5.5, "Vadodara, Gujarat, India"),
    "rajkot": (22.3039, 70.8022, 5.5, "Rajkot, Gujarat, India"),
    "panaji": (15.4909, 73.8278, 5.5, "Panaji, Goa, India"),
    "goa": (15.2993, 74.1240, 5.5, "Goa, India"),

    # Kerala
    "kochi": (9.9312, 76.2673, 5.5, "Kochi, Kerala, India"),
    "cochin": (9.9312, 76.2673, 5.5, "Kochi, Kerala, India"),
    "thiruvananthapuram": (8.5241, 76.9366, 5.5, "Thiruvananthapuram, Kerala, India"),
    "trivandrum": (8.5241, 76.9366, 5.5, "Thiruvananthapuram, Kerala, India"),
    "kozhikode": (11.2588, 75.7804, 5.5, "Kozhikode, Kerala, India"),
    "calicut": (11.2588, 75.7804, 5.5, "Kozhikode, Kerala, India"),
    "thrissur": (10.5276, 76.2144, 5.5, "Thrissur, Kerala, India"),

    # International Hubs
    "london": (51.5074, -0.1278, 0.0, "London, United Kingdom"),
    "new york": (40.7128, -74.0060, -5.0, "New York, NY, USA"),
    "san francisco": (37.7749, -122.4194, -8.0, "San Francisco, CA, USA"),
    "chicago": (41.8781, -87.6298, -6.0, "Chicago, IL, USA"),
    "dallas": (32.7767, -96.7970, -6.0, "Dallas, TX, USA"),
    "toronto": (43.6532, -79.3832, -5.0, "Toronto, Ontario, Canada"),
    "vancouver": (49.2827, -123.1207, -8.0, "Vancouver, BC, Canada"),
    "dubai": (25.2048, 55.2708, 4.0, "Dubai, United Arab Emirates"),
    "abu dhabi": (24.4539, 54.3773, 4.0, "Abu Dhabi, United Arab Emirates"),
    "singapore": (1.3521, 103.8198, 8.0, "Singapore"),
    "kuala lumpur": (3.1390, 101.6869, 8.0, "Kuala Lumpur, Malaysia"),
    "sydney": (-33.8688, 151.2093, 10.0, "Sydney, Australia"),
    "melbourne": (-37.8136, 144.9631, 10.0, "Melbourne, Australia"),
}


def lookup_city(city_query: str) -> Optional[Tuple[float, float, float, str]]:
    """
    Looks up city latitude, longitude, timezone offset, and formal name.
    Matches exact or substring keywords.
    Returns (lat, lon, tz_offset, canonical_name) or None.
    """
    if not city_query:
        return None

    q = city_query.strip().lower()

    # Exact match
    if q in CITY_DATABASE:
        return CITY_DATABASE[q]

    # Substring match in keys
    for k, v in CITY_DATABASE.items():
        if k in q or q in k:
            return v

    # Check words
    parts = q.replace(",", " ").split()
    for word in parts:
        if len(word) >= 3 and word in CITY_DATABASE:
            return CITY_DATABASE[word]

    return None


def get_default_coordinates(place_name: str = "Bengaluru, Karnataka") -> Tuple[float, float, float, str]:
    """Fallback default coordinates (Bengaluru, IST)."""
    match = lookup_city(place_name)
    if match:
        return match
    return (12.9716, 77.5946, 5.5, place_name if place_name else "Bengaluru, Karnataka, India")

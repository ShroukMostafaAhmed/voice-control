// Smart Home Data Structure
const smartHomeData = {
    bathroom: {
        name: "Bathroom",
        devices: [
            { id: "bath_light", name: "Light system", type: "light", status: true },
            { id: "bath_fire", name: "Fire Alert", type: "sensor", status: false },
            { id: "bath_heater", name: "Water Heater", type: "heater", status: false },
            { id: "bath_fan", name: "Fan system", type: "fan", status: false }
        ]
    },
    corridors: {
        name: "Corridors - Eyes",
        devices: [
            { id: "corr_main_light", name: "Main Light", type: "light", status: false },
            { id: "corr_spots", name: "Spots Light", type: "light", status: false },
            { id: "corr_fire", name: "Fire Alert", type: "sensor", status: false }
        ]
    },
    reception: {
        name: "Reception",
        devices: [
            { id: "rec_light", name: "Light system", type: "light", status: false },
            { id: "rec_window", name: "Smart window", type: "window", status: false },
            { id: "rec_fire", name: "Fire Alert", type: "sensor", status: false },
            { id: "rec_sound", name: "Sound system", type: "sound", status: false },
            { id: "rec_ac", name: "Air Condition", type: "ac", status: false }
        ]
    },
    outdoor: {
        name: "Out Door",
        devices: [
            { id: "out_camera", name: "Camera system", type: "camera", status: true },
            { id: "out_light", name: "Light system", type: "light", status: false },
            { id: "out_door", name: "Smart Door", type: "door", status: false }
        ]
    },
    room1: {
        name: "Room 1",
        devices: [
            { id: "r1_ac", name: "Air condition", type: "ac", status: false },
            { id: "r1_tv", name: "TV", type: "tv", status: false },
            { id: "r1_light", name: "Light system", type: "light", status: true },
            { id: "r1_window", name: "Smart window", type: "window", status: false },
            { id: "r1_fire", name: "Fire Alert", type: "sensor", status: false },
            { id: "r1_sound", name: "Sound system", type: "sound", status: false }
        ]
    },
    kitchen: {
        name: "Kitchen",
        devices: [
            { id: "kit_light", name: "Light system", type: "light", status: false },
            { id: "kit_window", name: "Smart window", type: "window", status: false },
            { id: "kit_fan", name: "Fan system", type: "fan", status: false },
            { id: "kit_fire", name: "Fire Alert", type: "sensor", status: false }
        ]
    },
    room2: {
        name: "Room 2",
        devices: [
            { id: "r2_ac", name: "Air condition", type: "ac", status: false },
            { id: "r2_sound", name: "Sound system", type: "sound", status: false },
            { id: "r2_light", name: "Light system", type: "light", status: false },
            { id: "r2_fire", name: "Fire Alert", type: "sensor", status: false }
        ]
    }
};

// Device energy consumption (in watts)
const deviceEnergy = {
    light: 60,
    sensor: 5,
    heater: 2000,
    fan: 75,
    window: 10,
    sound: 50,
    camera: 15,
    door: 20,
    ac: 1500,
    tv: 150
};

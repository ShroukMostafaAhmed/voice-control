// Scenarios System
const scenarios = {
    fire: {
        name: "Fire Emergency",
        description: "Smoke detected in the building!",
        conditions: {
            smoke_detected: 1,
            danger_level: "critical"
        },
        actions: [
            "Turn on ALL lights for visibility",
            "Activate ALL fire alert sensors",
            "Turn off ALL heaters to prevent fire spread",
            "Turn off ALL AC units",
            "Open ALL windows for ventilation",
            "Turn off sound systems and TVs",
            "Turn on outdoor camera for monitoring",
            "Open outdoor door for emergency exit"
        ],
        devices: {
            // Turn on ALL lights
            bath_light: true,
            corr_main_light: true,
            corr_spots: true,
            rec_light: true,
            r1_light: true,
            r2_light: true,
            kit_light: true,
            out_light: true,
            
            // Activate ALL fire alerts
            bath_fire: true,
            corr_fire: true,
            rec_fire: true,
            r1_fire: true,
            kit_fire: true,
            r2_fire: true,
            
            // Turn off heaters and fans
            bath_heater: false,
            bath_fan: false,
            kit_fan: false,
            
            // Turn off AC units
            rec_ac: false,
            r1_ac: false,
            r2_ac: false,
            
            // Open ALL windows
            rec_window: true,
            r1_window: true,
            kit_window: true,
            
            // Turn off entertainment
            r1_tv: false,
            rec_sound: false,
            r1_sound: false,
            r2_sound: false,
            
            // Security
            out_camera: true,
            out_door: true
        },
        priority: "CRITICAL",
        color: "#ef4444"
    },
    
    hot: {
        name: "Hot Weather",
        description: "Temperature is very high (32°C+)",
        conditions: {
            temperature: 32,
            scenario: "hot_weather"
        },
        actions: [
            "Turn on ALL AC units",
            "Turn off heaters",
            "Open windows for air circulation",
            "Turn on fans",
            "Turn off unnecessary lights to reduce heat"
        ],
        devices: {
            // Turn on AC
            rec_ac: true,
            r1_ac: true,
            r2_ac: true,
            
            // Turn off heater
            bath_heater: false,
            
            // Open windows
            rec_window: true,
            r1_window: true,
            kit_window: true,
            
            // Turn on fans
            bath_fan: true,
            kit_fan: true,
            
            // Turn off some lights
            corr_spots: false,
            out_light: false
        },
        priority: "HIGH",
        color: "#f59e0b"
    },
    
    cold: {
        name: "Cold Weather",
        description: "Temperature is very low (15°C or below)",
        conditions: {
            temperature: 15,
            scenario: "cold_weather"
        },
        actions: [
            "Turn on bathroom heater",
            "Close all windows",
            "Turn off AC units",
            "Turn off fans",
            "Turn on corridor lights for warmth"
        ],
        devices: {
            // Turn on heater
            bath_heater: true,
            
            // Close windows
            rec_window: false,
            r1_window: false,
            kit_window: false,
            
            // Turn off AC
            rec_ac: false,
            r1_ac: false,
            r2_ac: false,
            
            // Turn off fans
            bath_fan: false,
            kit_fan: false,
            
            // Turn on some lights
            corr_main_light: true
        },
        priority: "MEDIUM",
        color: "#3b82f6"
    },
    
    night: {
        name: "Night Mode",
        description: "It's late at night (10 PM - 6 AM)",
        conditions: {
            hour: 23,
            scenario: "night_mode"
        },
        actions: [
            "Turn on bedroom lights (dim)",
            "Turn off corridor lights",
            "Turn off TVs",
            "Turn off sound systems",
            "Enable outdoor camera",
            "Lock outdoor door"
        ],
        devices: {
            // Bedroom lights on
            r1_light: true,
            r2_light: true,
            
            // Turn off other lights
            rec_light: false,
            kit_light: false,
            bath_light: false,
            corr_main_light: false,
            corr_spots: false,
            out_light: false,
            
            // Turn off entertainment
            r1_tv: false,
            rec_sound: false,
            r1_sound: false,
            r2_sound: false,
            
            // Security
            out_camera: true,
            out_door: false
        },
        priority: "MEDIUM",
        color: "#6366f1"
    },
    
    morning: {
        name: "Morning Routine",
        description: "Good morning! (6 AM - 9 AM)",
        conditions: {
            hour: 8,
            scenario: "morning_routine"
        },
        actions: [
            "Turn on bathroom light",
            "Turn on kitchen light",
            "Turn on corridor lights",
            "Turn on bathroom heater",
            "Open windows for fresh air",
            "Enable outdoor camera"
        ],
        devices: {
            // Morning lights
            bath_light: true,
            kit_light: true,
            corr_main_light: true,
            
            // Heater
            bath_heater: true,
            
            // Open windows
            rec_window: true,
            kit_window: true,
            
            // Security
            out_camera: true,
            out_door: true
        },
        priority: "MEDIUM",
        color: "#fbbf24"
    },
    
    away: {
        name: "Leaving Home",
        description: "Energy saving mode - nobody home",
        conditions: {
            user_present: 0,
            scenario: "energy_saving"
        },
        actions: [
            "Turn off ALL lights",
            "Turn off ALL AC units",
            "Turn off heater",
            "Turn off ALL fans",
            "Turn off TVs and sound systems",
            "Close all windows",
            "Enable outdoor camera",
            "Lock outdoor door",
            "Turn off fire alerts to save energy"
        ],
        devices: {
            // Turn off ALL lights
            bath_light: false,
            corr_main_light: false,
            corr_spots: false,
            rec_light: false,
            r1_light: false,
            r2_light: false,
            kit_light: false,
            out_light: false,
            
            // Turn off heater and fans
            bath_heater: false,
            bath_fan: false,
            kit_fan: false,
            
            // Turn off AC
            rec_ac: false,
            r1_ac: false,
            r2_ac: false,
            
            // Turn off entertainment
            r1_tv: false,
            rec_sound: false,
            r1_sound: false,
            r2_sound: false,
            
            // Close windows
            rec_window: false,
            r1_window: false,
            kit_window: false,
            
            // Turn off fire alerts
            bath_fire: false,
            corr_fire: false,
            rec_fire: false,
            r1_fire: false,
            kit_fire: false,
            r2_fire: false,
            
            // Security
            out_camera: true,
            out_door: false
        },
        priority: "LOW",
        color: "#8b5cf6"
    }
};

// Initialize scenarios
document.addEventListener('DOMContentLoaded', () => {
    const scenarioBtns = document.querySelectorAll('.scenario-btn');
    const responseDiv = document.getElementById('scenario-response');
    const clearFireBtn = document.getElementById('clear-fire-btn');
    
    // Clear fire emergency button
    if (clearFireBtn) {
        clearFireBtn.addEventListener('click', async () => {
            // Turn off all fire sensors
            for (const roomKey in smartHomeData) {
                smartHomeData[roomKey].devices.forEach(async device => {
                    if (device.id.includes('fire') && device.status) {
                        if (typeof aiClient !== 'undefined') {
                            await aiClient.controlDevice(device.id, 'off');
                        }
                        device.status = false;
                    }
                });
            }
            
            // Clear fire emergency flag
            if (typeof window !== 'undefined') {
                window.fireEmergencyActive = false;
            }
            
            // Update UI
            if (typeof app !== 'undefined' && app.renderRooms) {
                app.renderRooms();
            }
            if (typeof apartment3D !== 'undefined' && apartment3D) {
                apartment3D.updateDeviceStates();
            }
            
            // Hide button
            clearFireBtn.style.display = 'none';
            
            // Show message
            responseDiv.innerHTML = `
                <strong>✅ Fire Emergency Cleared</strong>
                <p>All fire alarms have been turned off. The situation is under control.</p>
            `;
            responseDiv.classList.add('show');
            responseDiv.style.borderColor = '#10b981';
            
            if (typeof voiceControl !== 'undefined') {
                voiceControl.speak("Fire emergency cleared. All alarms turned off.");
            }
        });
    }
    
    scenarioBtns.forEach(btn => {
        btn.addEventListener('click', async () => {
            const scenarioType = btn.getAttribute('data-scenario');
            const scenario = scenarios[scenarioType];
            
            if (!scenario) return;
            
            // Show initial response
            responseDiv.innerHTML = `
                <strong>🎬 Scenario: ${scenario.name}</strong>
                <p><em>${scenario.description}</em></p>
                <p><strong>Priority:</strong> ${scenario.priority}</p>
                <p style="margin-top: 10px; opacity: 0.8;">Analyzing situation...</p>
            `;
            responseDiv.classList.add('show');
            responseDiv.style.borderColor = scenario.color;
            
            // Speak the scenario description
            if (typeof voiceControl !== 'undefined') {
                const announcement = `Alert! ${scenario.name}. ${scenario.description}. Priority level: ${scenario.priority}. Analyzing situation and taking appropriate actions.`;
                voiceControl.speak(announcement);
                
                // Wait for speech to finish
                await new Promise(resolve => setTimeout(resolve, 5000));
            }
            
            // Update UI with actions
            responseDiv.innerHTML = `
                <strong>🎬 Scenario: ${scenario.name}</strong>
                <p><em>${scenario.description}</em></p>
                <p><strong>Priority:</strong> ${scenario.priority}</p>
                <p><strong>Actions to be taken:</strong></p>
                <ul>
                    ${scenario.actions.map(action => `<li>${action}</li>`).join('')}
                </ul>
                <p style="margin-top: 10px; opacity: 0.8;">Executing actions now...</p>
            `;
            
            // Speak each action
            if (typeof voiceControl !== 'undefined') {
                for (let i = 0; i < scenario.actions.length; i++) {
                    const action = scenario.actions[i];
                    voiceControl.speak(`Action ${i + 1}: ${action}`);
                    await new Promise(resolve => setTimeout(resolve, 3000));
                }
            }
            
            // Execute device changes
            try {
                let devicesChanged = 0;
                
                // Check if this is fire scenario
                const isFireScenario = scenarioType === 'fire';
                
                // Set global fire emergency flag
                if (typeof window !== 'undefined') {
                    window.fireEmergencyActive = isFireScenario;
                    
                    // Show clear fire button if fire scenario
                    const clearFireBtn = document.getElementById('clear-fire-btn');
                    if (clearFireBtn && isFireScenario) {
                        clearFireBtn.style.display = 'block';
                    }
                }
                
                // Execute devices one by one to ensure proper updates
                for (const [deviceId, status] of Object.entries(scenario.devices)) {
                    // Find device in smartHomeData
                    let found = false;
                    for (const roomKey in smartHomeData) {
                        const device = smartHomeData[roomKey].devices.find(d => d.id === deviceId);
                        if (device) {
                            found = true;
                            devicesChanged++;
                            
                            // Update device using aiClient (same as Control Panel)
                            const action = status ? 'on' : 'off';
                            
                            if (typeof aiClient !== 'undefined') {
                                const result = await aiClient.controlDevice(deviceId, action);
                                if (result.success) {
                                    console.log(`✓ ${deviceId} set to ${action}`);
                                }
                            }
                            
                            // Update local data
                            device.status = status;
                            
                            // Start fire alarm sound immediately for fire sensors during fire scenario
                            if (isFireScenario && deviceId.includes('fire') && status) {
                                if (typeof deviceSounds !== 'undefined') {
                                    await deviceSounds.playFireAlarm(deviceId);
                                    console.log(`🚨 FIRE ALARM ACTIVATED: ${deviceId}`);
                                } else {
                                    console.error('❌ deviceSounds not available!');
                                }
                            }
                            
                            // Small delay between devices for visual effect
                            await new Promise(resolve => setTimeout(resolve, 100));
                            break;
                        }
                    }
                }
                
                // Force UI update in Control Panel
                if (typeof app !== 'undefined' && app.renderRooms) {
                    app.renderRooms();
                }
                
                // Update 3D simulation
                if (typeof apartment3D !== 'undefined' && apartment3D) {
                    apartment3D.updateDeviceStates();
                }
                
                // Small delay to ensure visual updates
                await new Promise(resolve => setTimeout(resolve, 300));
                
                // Update response with success
                responseDiv.innerHTML = `
                    <strong>✅ Scenario: ${scenario.name}</strong>
                    <p><em>${scenario.description}</em></p>
                    <p><strong>Priority:</strong> ${scenario.priority}</p>
                    <p><strong>Actions Completed:</strong></p>
                    <ul>
                        ${scenario.actions.map(action => `<li>✓ ${action}</li>`).join('')}
                    </ul>
                    <p style="margin-top: 10px; color: #10b981; font-weight: 600;">
                        ✓ All ${devicesChanged} devices controlled successfully!
                    </p>
                `;
                
                // Speak completion
                if (typeof voiceControl !== 'undefined') {
                    const completion = `All actions completed successfully. ${devicesChanged} devices have been controlled. The situation is now under control.`;
                    voiceControl.speak(completion);
                }
                
                // Clear fire emergency flag if not fire scenario
                if (scenarioType !== 'fire' && typeof window !== 'undefined') {
                    window.fireEmergencyActive = false;
                }
                
            } catch (error) {
                console.error('Error executing scenario:', error);
                responseDiv.innerHTML += `<p style="color: #ef4444; margin-top: 10px;">Error: ${error.message}</p>`;
                
                if (typeof voiceControl !== 'undefined') {
                    voiceControl.speak("Error occurred while executing actions. Please check the system.");
                }
                
                // Clear fire emergency flag on error
                if (typeof window !== 'undefined') {
                    window.fireEmergencyActive = false;
                }
            }
        });
    });
});

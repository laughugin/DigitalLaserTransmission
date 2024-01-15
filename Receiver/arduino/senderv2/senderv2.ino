const int sensorPin = A2;  // Analog input pin
bool data[1300];
float end = 1300;
String output = "";
int threshold = 800;
unsigned long lastPrintTime = 0;  // Variable to store the last print time
bool isFirstMessage = true;  // Variable to track the first message after a delay

void setup() {
  Serial.begin(57600);
}

void loop() {
  int sensorValue = analogRead(sensorPin);
  if (sensorValue < threshold) {
    read();
    
    Serial.print(output.substring(2, 39));

    // Clear output and reset end
    output = "";
    end = 1300;

    // Update last print time
    lastPrintTime = millis();
    isFirstMessage = false;
    delay(35);
  } else {
    
    // Check if enough time has passed to start a new line
    if (!isFirstMessage && millis() - lastPrintTime >= 1000) {
      Serial.println();  // Print a new line if it's not the first message
      isFirstMessage = true;  // Set isFirstMessage to true after the first message
    }
  }
}

void read() {
  float c = 0;
  for (int i = 0; i < 1300; i++) {
    int sensorData = analogRead(sensorPin);
    if (sensorData < threshold) {
      data[i] = true;
      c = c + 1;
    } else {
      data[i] = false;
      c = 0;
    }
    if (c > 71) {
      end = i;
      break;
    }
    delay(2);
  }
  c = 0;
  for (int i = 0; i < 50; i++) {
    for (int j = 0; j < round(end / 50); j++) {
      if (data[round(i * end / 50) + j]) {
        c = c + 1;
      }
    }
    float temp = c / (end / 50);
    output = output + String(round(temp));
    c = 0;
  }
}

const int laserPin = A2;  // Output pin
const int chunkSize = 38; // Number of characters in each chunk

void setup() {
  Serial.begin(57600);
  Serial.setTimeout(100);
  pinMode(laserPin, OUTPUT);
}

void loop() {  
  if (Serial.available() > 0) {
    String data = "";
    
    data = Serial.readString();
    
    if (data == "") {
      
      return;
    } 
    
    if (data == "laser_on") {
      digitalWrite(laserPin, HIGH);
      return;
    }
    
    if (data == "laser_off"){
      digitalWrite(laserPin, LOW);
      return;
    }

    digitalWrite(laserPin, LOW);
    delay(300);
    
    int numChunks = (data.length() + chunkSize) / chunkSize;

    for (int chunk = 0; chunk < numChunks; chunk++) {
      int startIdx = chunk * (chunkSize - 1);
      int endIdx = startIdx + chunkSize;
      String chunkData = data.substring(startIdx, endIdx);
      
      chunkData = "11" + chunkData + "0111111111";

      for (int i = 0; i < chunkData.length(); i++) {
        if (chunkData[i] == '0') {
          digitalWrite(laserPin, LOW);
        } else {
          digitalWrite(laserPin, HIGH);
        }
        delay(17);
      }
      digitalWrite(laserPin, LOW);
      delay(300);
    }
  }
}

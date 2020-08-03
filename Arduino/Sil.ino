int rooms = 2;

// Led pin
int ledPins[] = {6,7};

// Pir pin
int pirPins[] = {3,4};

// Lettura valori sensori
int vals[] = {0,0};

// Pir state and time
int pirState[] = {false, false}; 
int pirPrevState[] = {false, false};
int pirTime[] = {0,0};

// The time we give the sensor to calibrate (10-60 secs according to the datasheet)
int calibrationTime = 30;

// Input from app
bool manualMode = false;

int timeOutMillis = 10000;

void setup() {
  for(int i = 0; i < rooms; i++){
    pinMode(ledPins[i], OUTPUT);  
    pinMode(pirPins[i], INPUT);  
  }
   
  Serial.begin(9600);
   
  for(int i = 0; i < calibrationTime; i++) delay(1000);
  delay(500);
}
 
void loop(){
  int nowTime = millis();

  if(! manualMode){
    // Detect movement 
    // Update state and time
    // Update light active
    for(int i = 0; i < rooms; i++){
      vals[i] = digitalRead(pirPins[i]);
      if(vals[i] == HIGH){
        pirState[i] = true;
        pirTime[i] = nowTime;
      }
    }
    
    // Check for timeout
    for(int i = 0; i < rooms; i++) if(nowTime - pirTime[i] > timeOutMillis) pirState[i] = false;      
  }
  
  // comunication
  //      || codeOp1 codeOp0 || LightId4..0 || Switch0 ||
  // bit  ||  7,      6      ||     5,..,1  ||     0   ||
  // codeOp 0 -> modify from automatic to manual mode
  // codeOp 1 -> turn on/off light 
  // codeOp 2,3 -> not used

  byte manual_mode_id = 1;
  byte auto_mode_id = 0;
  byte light1_on_id = 67;
  byte light1_off_id = 66;
  byte light2_on_id = 65;
  byte light2_off_id = 64;
  
  if (Serial.available() > 0) {
    byte info = Serial.read();
    int codeOp = 2 * bitRead(info,7) + bitRead(info,6);
    int switchState = bitRead(info,0);
    switch(codeOp){
      case 0:
        manualMode = switchState;            
        break;
      case 1:
        int lightId = 16 * bitRead(info,5) + 8 * bitRead(info,4) + 4 * bitRead(info,3) + 2 * bitRead(info,2) + bitRead(info,1);
        if(manualMode && lightId < rooms) pirState[lightId] = switchState;
        break;
      /*default:
        break;*/
    }
  }

  // set led only if switch state
  for(int i = 0; i < rooms; i++){ 
    byte bts = 64 + 2*i;
    if(pirState[i] && !pirPrevState[i]){ // now True, prev False
      digitalWrite(ledPins[i], HIGH);
      bitSet(bts, 0);
      Serial.write(bts);
    }
    if(!pirState[i] && pirPrevState[i]){ // now False, prev True
      digitalWrite(ledPins[i], LOW);
      Serial.write(bts);
    }
    pirPrevState[i] = pirState[i];
  }
}

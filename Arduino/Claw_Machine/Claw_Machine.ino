// Connections to A4988
const int dirPin = 5;  // Direction
const int stepPin = 2; // Step

const int dirPin2 = 6;  // Direction
const int stepPin2 = 3; // Step

const int dirPin3 = 7;  // Direction
const int stepPin3 = 4; // Step

const int buttonPin = 9;
const int pawPin = 10;

const int xenabledPin = 8;

// Motor steps per rotation
const int STEPS_PER_REV = 6400;
const int Speed = 200;
//馬達圈數
const float range = 5;
const float spin_LR = 0.01 * range;
const float spin_FB = 0.01 * range;
const float spin_UD = 1.5;
const float spin_init = 4.25;

float count_LR = 0;//左右約8圈
float count_FB = 0;//前後4.5圈
float count_UD = 0;

boolean lastButtonState = LOW;
boolean ledState = LOW;
byte click = 0;

String serialData;

void setup() {

  // Setup the pins as Outputs
  pinMode(buttonPin, INPUT);
  pinMode(pawPin, OUTPUT);

  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  pinMode(stepPin3, OUTPUT);
  pinMode(dirPin3, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(xenabledPin, OUTPUT);
  digitalWrite(xenabledPin, LOW);
  digitalWrite(11, HIGH);

  Serial.begin(9600);

  init_paw();
}
void loop() {
  if (Serial.available()) {
    serialData = Serial.readStringUntil('\n');
    //Serial.println("open");

    if (serialData == "8" && count_FB < 4.5) {
      forward();
      Serial.println("forward");

    }
    if (serialData == "2" && count_FB > 0) {
      backward();
      Serial.println("backward");

    }
    if (serialData == "4" && count_LR > 0) {
      left();
      Serial.println("left");

    }
    if (serialData == "6" && count_LR < 8) {
      right();
      Serial.println("right");

    }
    if (serialData == "u" ) {
      paw_up();

    }
    if (serialData == "d") {
      paw_down();

    }

  }
  boolean reading1 = digitalRead(buttonPin); // 先讀一次

  if (reading1 != lastButtonState) { // 如果發現有改變
    delay(20); // <- de-bouncing, wait & read again 等 20ms 後再讀一次

    boolean reading2 = digitalRead(buttonPin);

    if (reading2 == reading1) { // 如果 20ms 後都一樣, 判定更改生效
      lastButtonState = reading2;
      click++; // click +1, 然後釋放按鈕的時候, 會再進來一次. 所以 click 會加至 =2
    } // else means reading2 is bouncing
  }

  if (click == 2) {
    click = 0;
    ledState = !ledState;
    button_click();
  }

}

void left() {
  count_LR -= spin_LR;
  digitalWrite(dirPin, HIGH);

  for (int x = 0; x < STEPS_PER_REV * spin_LR; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(Speed);
  }
}

void right() {
  count_LR += spin_LR;
  digitalWrite(dirPin, LOW);

  for (int x = 0; x < STEPS_PER_REV * spin_LR; x++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(Speed);
  }
}

void forward() {
  count_FB += spin_FB;
  digitalWrite(dirPin2, HIGH);

  for (int x = 0; x < STEPS_PER_REV * spin_FB; x++) {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(Speed);
  }
}

void backward() {
  count_FB -= spin_FB;
  digitalWrite(dirPin2, LOW);

  for (int x = 0; x < STEPS_PER_REV * spin_FB; x++) {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(Speed);
  }
}





void button_click() {

  paw_down();
  Serial.println("down");
  paw_close();
  Serial.println("paw_close");
  paw_up();
  Serial.println("up");
  while (count_LR > 0) {
    left();
    Serial.println("left");
  }
  while (count_FB > 0) {
    backward();
    Serial.println("backward");
  }

  paw_open();
  Serial.println("paw_open");


}

void paw_up() {
  digitalWrite(dirPin3, HIGH);

  for (int x = 0; x < STEPS_PER_REV * spin_UD; x++) {
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(Speed);
  }
}

void paw_down() {
  digitalWrite(dirPin3, LOW);

  for (int x = 0; x < STEPS_PER_REV * spin_UD; x++) {
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(Speed);
  }
}

void init_paw() {
  digitalWrite(dirPin3, HIGH);

  for (int x = 0; x < STEPS_PER_REV * spin_init; x++) {
    digitalWrite(stepPin3, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPin3, LOW);
    delayMicroseconds(Speed);
  }
}

void paw_close() {
  digitalWrite(pawPin, HIGH);
}

void paw_open() {
  digitalWrite(pawPin, LOW);
}

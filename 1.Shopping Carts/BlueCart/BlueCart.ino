#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);

int count = 0;
char input[12];
double total = 0;
int count_prod = 0;

int Button1 = 2;
int Button2 = 3;
int LED1 = 5;
int LED2 = 7;
int Button1Value = 0;
int Button2Value = 0;

void setup() {
  pinMode(Button1, INPUT);
  pinMode(Button2, INPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED1, OUTPUT);
  Serial.begin(9600);
  Serial1.begin(9600);
  lcd.begin();
  lcd.backlight();
  lcdbegin();
}

void lcdbegin() {
  lcd.setCursor(0, 0);
  lcd.print(" AUTOMATIC BILL");
  delay(2000);
  lcd.setCursor(0, 1);
  lcd.print("  SHOPPING CART       ");
  delay(2000);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   WELCOME TO ");
  lcd.setCursor(0, 1);
  lcd.print("   SMART STORE");
}

void items() {
  if (Serial1.available()) {
    count = 0;
    while (Serial1.available() && count < 12) {
      input[count] = Serial1.read();
      count++;
      delay(5);
    }

    if (input[0] == '1' && input[1] == '3' && input[2] == '0' && input[3] == '0' && input[4] == 'A' && input[5] == '2' && input[6] == '8' && input[7] == '7' && input[8] == '5' && input[9] == '6' && input[10] == '6' && input[11] == '0') {
      if (Button1Value == LOW) {
        lcd.clear();
        lcd.print("Chips Added       ");
        lcd.setCursor(0, 1);
        lcd.print("Price:25.00      ");
        delay(1500);
        total = total + 25.00;
        count_prod++;
        lcd.clear();
        lcd.print("Price(T) : ");
        lcd.print(total);
        lcd.setCursor(0, 1);
        lcd.print("Items  ");
        lcd.print(count_prod);
      } else {
        Serial.println("Chips Removed");
        lcd.clear();
        lcd.print("Chips Removed       ");
        lcd.setCursor(0, 1);
        lcd.print("Price :25.00      ");
        delay(1000);
        total = total - 25.00;
        count_prod--;
        lcd.clear();
        lcd.print("Price(T) : ");
        lcd.print(total);
        lcd.setCursor(0, 1);
        lcd.print("Items  ");
        lcd.print(count_prod);
      }
    }

    if (input[0] == '1' && input[1] == '4' && input[2] == '0' && input[3] == '0' && input[4] == '4' && input[5] == '8' && input[6] == 'E' && input[7] == 'F' && input[8] == '9' && input[9] == 'C' && input[10] == '2' && input[11] == 'F') {
      if (Button1Value == LOW) {
        lcd.clear();
        lcd.print("Maggi Added       ");
        lcd.setCursor(0, 1);
        lcd.print("Price :12.00      ");
        delay(1500);
        total = total + 12.00;
        count_prod++;
        lcd.clear();
        lcd.print("Price(T) : ");
        lcd.print(total);
        lcd.setCursor(0, 1);
        lcd.print("Items  ");
        lcd.print(count_prod);

      } else {
        lcd.clear();
        lcd.print("Maggi Removed       ");
        lcd.setCursor(0, 1);
        lcd.print("Price :12.00      ");
        delay(1000);
        total = total - 12.00;
        count_prod--;
        lcd.clear();
        lcd.print("Price(T) : ");
        lcd.print(total);
        lcd.setCursor(0, 1);
        lcd.print("Items  ");
        lcd.print(count_prod);
      }
    }
    if (input[0] == '1' && input[1] == '4' && input[2] == '0' && input[3] == '0' && input[4] == '4' && input[5] == '8' && input[6] == 'E' && input[7] == 'F' && input[8] == '9' && input[9] == '2' && input[10] == '2' && input[11] == '1') {
      if (Button1Value == LOW) {
        lcd.clear();
        lcd.print("Chololate Added       ");
        lcd.setCursor(0, 1);
        lcd.print("Price(Rm):20.00      ");
        delay(1500);
        total = total + 20.00;
        count_prod++;
        lcd.clear();
        lcd.print("Price(T) : ");
        lcd.print(total);
        lcd.setCursor(0, 1);
        lcd.print("Items  ");
        lcd.print(count_prod);

      } else {
        lcd.clear();
        lcd.print("Chololate Removed       ");
        lcd.setCursor(0, 1);
        lcd.print("Price :20.00      ");
        delay(1000);
        total = total - 20.00;
        count_prod--;
        lcd.clear();
        lcd.print("Price(T) : ");
        lcd.print(total);
        lcd.setCursor(0, 1);
        lcd.print("Items  ");
        lcd.print(count_prod);
      }
    }
    if (input[0] == '1' && input[1] == '4' && input[2] == '0' && input[3] == '0' && input[4] == '4' && input[5] == '6' && input[6] == 'E' && input[7] == 'E' && input[8] == '1' && input[9] == '9' && input[10] == 'A' && input[11] == '5') {
      if (Button1Value == LOW) {
        lcd.clear();
        lcd.print("Biscuit Added       ");
        lcd.setCursor(0, 1);
        lcd.print("Price(Rm):10.00      ");
        delay(1500);
        total = total + 10.00;
        count_prod++;
        lcd.clear();
        lcd.print("Price(T) : ");
        lcd.print(total);
        lcd.setCursor(0, 1);
        lcd.print("Items  ");
        lcd.print(count_prod);

      } else {
        lcd.clear();
        lcd.print("Biscuit Removed       ");
        lcd.setCursor(0, 1);
        lcd.print("Price(Rm):10.00      ");
        delay(1000);
        total = total - 10.00;
        count_prod--;
        lcd.clear();
        lcd.print("Price(T) : ");
        lcd.print(total);
        lcd.setCursor(0, 1);
        lcd.print("Items  ");
        lcd.print(count_prod);
      }
    }
  }
}

void loop() {
  Button1Value = digitalRead(Button1);
  //Button2Value = digitalRead(Button2);
  items();
  if (Button2Value == 1) {
    lcd.clear();
    lcd.print("Thank you");
    lcd.setCursor(0, 1);
    lcd.print("Shopping");
    delay(1000);
    lcd.clear();
    lcd.print("Please proceed");
    lcd.setCursor(0, 1);
    lcd.print("to bill counter");
    delay(2000);
    lcdbegin();
    total = 0;
    count_prod = 0;
    items();
  }
}
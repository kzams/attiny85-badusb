#include "DigiKeyboard.h"

void setup() {
  DigiKeyboard.sendKeyStroke(0);  // Początek
  DigiKeyboard.delay(1000);

  DigiKeyboard.sendKeyStroke(KEY_R, MOD_GUI_LEFT); // Win+R
  DigiKeyboard.delay(500);

  DigiKeyboard.print("powershell");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
  DigiKeyboard.delay(1000);

  DigiKeyboard.print("Start-Process notepad");
  DigiKeyboard.sendKeyStroke(KEY_ENTER);
}

void loop() {}

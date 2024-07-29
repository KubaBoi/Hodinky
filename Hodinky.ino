// An Arduino based framework for the Lilygo T-Watch 2020
// Much of the code is based on the sample apps for the
// T-watch that were written and copyrighted by Lewis He.
//(Copyright (c) 2019 lewis he)

#include "config.h"
#include <soc/rtc.h>

TTGOClass *ttgo;

uint32_t targetTime = 0;       // for next 1 second display update
// uint32_t clockUpTime = 0;      // track the time the clock is displayed

uint8_t hh, mm, ss, mmonth, dday; // H, M, S variables
uint16_t yyear; // Year is 16 bit int

uint8_t wakeTime = 0;

void setup() {
  //initSetup();
  ttgo = TTGOClass::getWatch();
  ttgo->begin();
  ttgo->tft->setTextFont(1);
  ttgo->tft->fillScreen(TFT_BLACK);
  ttgo->tft->setTextColor(TFT_YELLOW, TFT_BLACK); // Note: the new fonts do not draw the background colour
  //Initialize lvgl
  ttgo->lvgl_begin();

  //Check if the RTC clock matches, if not, use compile time
  ttgo->rtc->check();

  //Synchronize time to system time
  ttgo->rtc->syncToSystem();
  
  displayTime(true); // Our GUI to show the time
  ttgo->openBL(); // Turn on the backlight

}

void loop() {

  if (targetTime < millis()) {
    targetTime = millis() + 1000;
    displayTime(ss == 0); // Call every second but only update time every minute
    if (ttgo->power->getVbusCurrent() > 0) wakeTime = 0;
    
    wakeTime++;
    if (wakeTime == 10) ttgo->setBrightness(50); 
    else if (wakeTime == 20) ttgo->closeBL();
    else if (wakeTime >= 30) {
      wakeTime = 0;
      ttgo->displaySleep();
      ttgo->powerOff();
      esp_sleep_enable_ext1_wakeup(GPIO_SEL_38, ESP_EXT1_WAKEUP_ALL_LOW);
      esp_deep_sleep_start();
    }
  }

  int16_t x, y;
  if (ttgo->getTouch(x, y)) {
    wakeTime = 0;
    ttgo->setBrightness(100);
    ttgo->openBL();
    
    while (ttgo->getTouch(x, y)) {} // wait for user to release 

    /*switch (modeMenu()) { // Call modeMenu. The return is the desired app number
      case 0: // Zero is the clock, just exit the switch
        break;
      case 1:
        jSats();
        break;
      case 2:
        appAccel();
        break;
      case 3:
        appBattery();
        break;
      case 4:
        appTouch();
        break;
      case 5:
        appSetTime();
        break;
    }*/
    displayTime(true);
  }
}

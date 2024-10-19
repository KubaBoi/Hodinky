
#include "config.h"
#include <soc/rtc.h>

TTGOClass *ttgo;

uint32_t targetTime = 0; // for next 1 second display update
// uint32_t clockUpTime = 0;      // track the time the clock is displayed

uint8_t hh, mm, ss, mmonth, dday; // H, M, S variables
uint16_t yyear;                   // Year is 16 bit int

uint8_t wakeTime = 0;

void setup()
{
    // initSetup();
    ttgo = TTGOClass::getWatch();
    ttgo->begin();
    ttgo->tft->setTextFont(2);
    ttgo->tft->fillScreen(TFT_BLACK);
    ttgo->tft->setTextColor(TFT_WHITE, TFT_BLACK); // Note: the new fonts do not draw the background colour
    // Initialize lvgl
    ttgo->lvgl_begin();

    // Check if the RTC clock matches, if not, use compile time
    ttgo->rtc->check();

    // Synchronize time to system time
    ttgo->rtc->syncToSystem();
    ttgo->openBL(); // Turn on the backlight
}

int a = 0;
void loop()
{
    ttgo->tft->setCursor(0, 0);

    asm volatile(
        "movi a8, 0x1 \n"
        "add %[output], %[input], a8 \n"
        : [output] "=r"(a)
        : [input] "r"(a)
        : "a8");

    ttgo->tft->print(a);
}
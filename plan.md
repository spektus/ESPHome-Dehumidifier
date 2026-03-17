1. Add a helper function `applyTimerToStatus` in `MideaDehumComponent` to abstract the timer construction logic.
2. The helper function `applyTimerToStatus(uint8_t* setStatusCommand)` should encompass the logic currently within the `#ifdef USE_MIDEA_DEHUM_TIMER` block in `sendSetStatus`.
3. Use the helper function in `sendSetStatus`.

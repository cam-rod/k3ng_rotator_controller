/*---------------------- macros - don't touch these unless you know what you are doing ---------------------*/
#define CONFIGURATION_STRUCT_VERSION 123

#define AZ 1
#define EL 2
 
#define DIR_CCW 0x10                      // CW Encoder Code (Do not change)
#define DIR_CW 0x20                       // CCW Encoder Code (Do not change)

#define BRAKE_RELEASE_OFF 0
#define BRAKE_RELEASE_ON 1

//az_state
#define IDLE 0
#define SLOW_START_CW 1
#define SLOW_START_CCW 2
#define NORMAL_CW 3
#define NORMAL_CCW 4
#define SLOW_DOWN_CW 5
#define SLOW_DOWN_CCW 6
#define INITIALIZE_SLOW_START_CW 7
#define INITIALIZE_SLOW_START_CCW 8
#define INITIALIZE_TIMED_SLOW_DOWN_CW 9
#define INITIALIZE_TIMED_SLOW_DOWN_CCW 10
#define TIMED_SLOW_DOWN_CW 11
#define TIMED_SLOW_DOWN_CCW 12
#define INITIALIZE_DIR_CHANGE_TO_CW 13
#define INITIALIZE_DIR_CHANGE_TO_CCW 14
#define INITIALIZE_NORMAL_CW 15
#define INITIALIZE_NORMAL_CCW 16

//el_state
#define SLOW_START_UP 1
#define SLOW_START_DOWN 2
#define NORMAL_UP 3
#define NORMAL_DOWN 4
#define SLOW_DOWN_DOWN 5
#define SLOW_DOWN_UP 6
#define INITIALIZE_SLOW_START_UP 7
#define INITIALIZE_SLOW_START_DOWN 8
#define INITIALIZE_TIMED_SLOW_DOWN_UP 9
#define INITIALIZE_TIMED_SLOW_DOWN_DOWN 10
#define TIMED_SLOW_DOWN_UP 11
#define TIMED_SLOW_DOWN_DOWN 12
#define INITIALIZE_DIR_CHANGE_TO_UP 13
#define INITIALIZE_DIR_CHANGE_TO_DOWN 14
#define INITIALIZE_NORMAL_UP 15
#define INITIALIZE_NORMAL_DOWN 16

//az_request & el_request
#define REQUEST_STOP 0
#define REQUEST_AZIMUTH 1
#define REQUEST_AZIMUTH_RAW 2
#define REQUEST_CW 3
#define REQUEST_CCW 4
#define REQUEST_UP 5
#define REQUEST_DOWN 6
#define REQUEST_ELEVATION 7
#define REQUEST_KILL 8

#define DEACTIVATE 0
#define ACTIVATE 1

#define CW 1
#define CCW 2
#define STOP_AZ 3
#define STOP_EL 4
#define UP 5
#define DOWN 6
#define STOP 7

//az_request_queue_state & el_request_queue_state
#define NONE 0
#define IN_QUEUE 1
#define IN_PROGRESS_TIMED 2
#define IN_PROGRESS_TO_TARGET 3

#define EMPTY 0
#define LOADED_AZIMUTHS 1
#define RUNNING_AZIMUTHS 2
#define LOADED_AZIMUTHS_ELEVATIONS 3
#define RUNNING_AZIMUTHS_ELEVATIONS 4

#define RED           0x1
#define YELLOW        0x3
#define GREEN         0x2
#define TEAL          0x6
#define BLUE          0x4
#define VIOLET        0x5
#define WHITE         0x7

#define LCD_UNDEF 0  
#define LCD_HEADING 1 
#define LCD_IDLE_STATUS 2
#define LCD_TARGET_AZ 3
#define LCD_TARGET_EL 4
#define LCD_TARGET_AZ_EL 5
#define LCD_ROTATING_CW 6
#define LCD_ROTATING_CCW 7
#define LCD_ROTATING_TO 8
#define LCD_ELEVATING_TO 9
#define LCD_ELEVATING_UP 10
#define LCD_ELEVATING_DOWN 11
#define LCD_ROTATING_AZ_EL 12
#define LCD_PARKED 13

#define ENCODER_IDLE          0
#define ENCODER_AZ_PENDING    1
#define ENCODER_EL_PENDING    2
#define ENCODER_AZ_EL_PENDING 3

#define NOT_DOING_ANYTHING 0
#define ROTATING_CW 1
#define ROTATING_CCW 2
#define ROTATING_UP 3
#define ROTATING_DOWN 4

#define REMOTE_UNIT_NO_COMMAND 0
#define REMOTE_UNIT_AZ_COMMAND 1
#define REMOTE_UNIT_EL_COMMAND 2
#define REMOTE_UNIT_OTHER_COMMAND 3
#define REMOTE_UNIT_AW_COMMAND 4
#define REMOTE_UNIT_DHL_COMMAND 5
#define REMOTE_UNIT_DOI_COMMAND 6
#define REMOTE_UNIT_CL_COMMAND 7
#define REMOTE_UNIT_RC_COMMAND 8
#define REMOTE_UNIT_GS_COMMAND 9
#define REMOTE_UNIT_RL_COMMAND 10
#define REMOTE_UNIT_RR_COMMAND 11
#define REMOTE_UNIT_RU_COMMAND 12
#define REMOTE_UNIT_RD_COMMAND 13
#define REMOTE_UNIT_RA_COMMAND 14
#define REMOTE_UNIT_RE_COMMAND 15
#define REMOTE_UNIT_RS_COMMAND 16
#define REMOTE_UNIT_PG_COMMAND 17

#define NOT_PARKED 0
#define PARK_INITIATED 1
#define PARKED 2

#define COORDINATES 1
#define MAIDENHEAD 2

#define FREE_RUNNING 0 
#define GPS_SYNC 1
#define RTC_SYNC 2
#define SLAVE_SYNC 3
#define SLAVE_SYNC_GPS 4
#define NOT_PROVISIONED 255

#define CONTROL_PORT0 1
#define ETHERNET_PORT0 2
#define ETHERNET_PORT1 4

#define CLIENT_INACTIVE 0
#define CLIENT_ACTIVE 1

#define LEFT 1
#define RIGHT 2
#define CENTER 3

#define STEPPER_UNDEF 0
#define STEPPER_CW 1
#define STEPPER_CCW 2
#define STEPPER_UP 3
#define STEPPER_DOWN 4

#define ETHERNET_SLAVE_DISCONNECTED 0
#define ETHERNET_SLAVE_CONNECTED 1

#define AUTOCORRECT_INACTIVE 0
#define AUTOCORRECT_WAITING_AZ 1
#define AUTOCORRECT_WAITING_EL 2
#define AUTOCORRECT_WATCHING_AZ 3
#define AUTOCORRECT_WATCHING_EL 4

#define AZ_DISPLAY_MODE_NORMAL 0
#define AZ_DISPLAY_MODE_RAW 1
#define AZ_DISPLAY_MODE_OVERLAP_PLUS 2

#define AUDIBLE_ALERT_SERVICE 0
#define AUDIBLE_ALERT_ACTIVATE 1
#define AUDIBLE_ALERT_SILENCE 2
#define AUDIBLE_ALERT_DISABLE 3
#define AUDIBLE_ALERT_ENABLE 4
#define AUDIBLE_ALERT_MANUAL_ACTIVATE 5



// for debugging 
#define DBG_PROCESS_REMOTE_SLAVE_COMMAND 43


#define DBG_CHECK_AZ_PRESET_POT 44
#define DBG_CHECK_PRESET_ENCODERS_NOT_IDLE 45

#define DBG_CHECK_PRESET_ENCODERS_PENDING 47

#define DBG_CHECK_AZ_MANUAL_ROTATE_LIMIT_CCW 49
#define DBG_CHECK_AZ_MANUAL_ROTATE_LIMIT_CW 50
#define DBG_CHECK_EL_MANUAL_ROTATE_LIMIT_DOWN 51
#define DBG_CHECK_EL_MANUAL_ROTATE_LIMIT_UP 52

#define DBG_CHECK_BUTTONS_BTN_CW 61
#define DBG_CHECK_BUTTONS_BTN_CCW 62
#define DBG_CHECK_BUTTONS_ADAFRUIT_STOP 63
#define DBG_CHECK_BUTTONS_RELEASE_NO_SLOWDOWN 64
#define DBG_CHECK_BUTTONS_RELEASE_KILL 65

#define DBG_PROCESS_DCU_1 233

#define DBG_STOP_ROTATION 238
#define DBG_SERVICE_SATELLITE_CLI_CMD_PREROTATE 239
#define DBG_BACKSLASH_GT_CMD 240
#define DBG_BACKSLASH_GC_CMD 241
#define DBG_CHECK_BUTTONS_SATELLITE 244
#define DBG_SERVICE_MOON_CLI_CMD 245
#define DBG_SERVICE_SUN_CLI_CMD 246
#define DBG_SERVICE_SATELLITE_CLI_CMD 247
#define DBG_SERVICE_SATELLITE_TRACKING 248
#define DBG_NEXTION_DATA_ENT_ENTER_PUSH_CALLBK 249
#define DBG_NEXTION_BUTTON 250
#define DBG_CHECK_BUTTONS_SUN 251
#define DBG_CHECK_BUTTONS_MOON 252
#define DBG_SERVICE_SUN_TRACKING 253
#define DBG_SERVICE_MOON_TRACKING 254

#define NEXTION_API_SYSTEM_CAPABILITIES_GS_232A 1
#define NEXTION_API_SYSTEM_CAPABILITIES_GS_232B 2
#define NEXTION_API_SYSTEM_CAPABILITIES_EASYCOM 4
#define NEXTION_API_SYSTEM_CAPABILITIES_DCU_1 8
#define NEXTION_API_SYSTEM_CAPABILITIES_ELEVATION 16
#define NEXTION_API_SYSTEM_CAPABILITIES_CLOCK 32
#define NEXTION_API_SYSTEM_CAPABILITIES_GPS 64
#define NEXTION_API_SYSTEM_CAPABILITIES_MOON 128
#define NEXTION_API_SYSTEM_CAPABILITIES_SUN 256
#define NEXTION_API_SYSTEM_CAPABILITIES_RTC 512
#define NEXTION_API_SYSTEM_CAPABILITIES_SATELLITE 1024
#define NEXTION_API_SYSTEM_CAPABILITIES_PARK 2048
#define NEXTION_API_SYSTEM_CAPABILITIES_AUTOPARK 4096
#define NEXTION_API_SYSTEM_CAPABILITIES_AUDIBLE_ALERT 8192

#define NEXTION_API_SYSTEM_CAPABILITIES_ENGLISH 1
#define NEXTION_API_SYSTEM_CAPABILITIES_SPANISH 2
#define NEXTION_API_SYSTEM_CAPABILITIES_CZECH 4
#define NEXTION_API_SYSTEM_CAPABILITIES_PORTUGUESE_BRASIL 8
#define NEXTION_API_SYSTEM_CAPABILITIES_GERMAN 16
#define NEXTION_API_SYSTEM_CAPABILITIES_FRENCH 32

#define DCU_1_SEMICOLON 1
#define DCU_1_CARRIAGE_RETURN 2

#define DEBUG_PROCESSES_SERVICE 1
#define DEBUG_PROCESSES_PROCESS_ENTER 2
#define DEBUG_PROCESSES_PROCESS_EXIT 3

#define PROCESS_LOOP 0
#define PROCESS_READ_HEADINGS 1
#define PROCESS_CHECK_SERIAL 2
#define PROCESS_SERVICE_NEXTION 3
#define PROCESS_UPDATE_LCD_DISPLAY 4
#define PROCESS_SERVICE_ROTATION 5
#define PROCESS_UPDATE_SUN_POSITION 6
#define PROCESS_UPDATE_MOON_POSITION 7
#define PROCESS_UPDATE_TIME 8
#define PROCESS_SERVICE_GPS 9
#define PROCESS_CHECK_FOR_DIRTY_CONFIGURATION 10
#define PROCESS_CHECK_BUTTONS 11
#define PROCESS_MISC_ADMIN 12
#define PROCESS_DEBUG 13

#define PROCESS_TABLE_SIZE 14

#define COORDINATE_PLANE_NORMAL 0
#define COORDINATE_PLANE_UPPER_LEFT_ORIGIN 1

#define DEACTIVATE_ALL 0
#define DEACTIVATE_MOON_TRACKING 1
#define DEACTIVATE_SUN_TRACKING 2
#define DEACTIVATE_SATELLITE_TRACKING 3
#define ACTIVATE_MOON_TRACKING 4
#define ACTIVATE_SUN_TRACKING 5
#define ACTIVATE_SATELLITE_TRACKING 6

// #define UPDATE_CURRENT_SAT_AZ_EL_NEXT_AOS_AND_LOS 0 //***
#define PRINT_AOS_LOS_MULTILINE_REPORT 1
#define PRINT_AOS_LOS_TABULAR_REPORT 2
// #define UPDATE_CURRENT_SAT_JUST_AZ_EL 3  //****
#define UPDATE_SAT_ARRAY_SLOT_AZ_EL_NEXT_AOS_LOS 4
#define UPDATE_SAT_ARRAY_SLOT_JUST_AZ_EL 5

#define DO_NOT_INCLUDE_RESPONSE_CODE 0
#define INCLUDE_RESPONSE_CODE 1

#define SERVICE_CALC_SERVICE 0
#define SERVICE_CALC_INITIALIZE 1
#define SERVICE_CALC_REPORT_STATE 2

#define SERVICE_CALC_DO_NOT_PRINT_DONE 0
#define SERVICE_CALC_PRINT_DONE 1

#define SERVICE_CALC_DO_NOT_PRINT_HEADER 0
#define SERVICE_CALC_PRINT_HEADER 1

#define CLOCK_DEFAULT_YEAR_AT_BOOTUP 2020
#define CLOCK_DEFAULT_MONTH_AT_BOOTUP 8
#define CLOCK_DEFAULT_DAY_AT_BOOTUP 15
#define CLOCK_DEFAULT_HOURS_AT_BOOTUP 0
#define CLOCK_DEFAULT_MINUTES_AT_BOOTUP 0
#define CLOCK_DEFAULT_SECONDS_AT_BOOTUP 0

#define DO_NOT_LOAD_HARDCODED_TLE 0
#define LOAD_HARDCODED_TLE 1

#define MAKE_IT_THE_CURRENT_SATELLITE 0
#define DO_NOT_MAKE_IT_THE_CURRENT_SATELLITE 1

#define NOT_VERBOSE 0
#define _VERBOSE_ 1

#define SERVICE_IDLE 0
#define SERVICE_CALC_IN_PROGRESS 1

#define VT100_CODE_CHAR_ATTR_OFF "[0m"
#define VT100_CODE_BLINK "[5m"
#define VT100_CLEAR_SCREEN "[2J"
#define VT100_CURSOR_UPPER_LEFT_CORNER "[f"
#define VT100_BOLD "[1m"

#define SOURCE_CONTROL_PORT 0
#define SOURCE_NEXTION 1

#define NEXTION_TRANSIENT_MESSAGE_IDLE 0
#define NEXTION_TRANSIENT_MESSAGE_REQUESTED 1
#define NEXTION_TRANSIENT_MESSAGE_IN_PROGRESS 2



/* ------end of macros ------- */
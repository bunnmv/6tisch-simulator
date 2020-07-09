# coding: utf-8

# === admin
NUM_SUFFICIENT_TX                           = 10      # sufficient num. of tx to estimate pdr by ACK
WAITING_FOR_TX                              = u'waiting_for_tx'
WAITING_FOR_RX                              = u'waiting_for_rx'

# === addressing
BROADCAST_ADDRESS                           = u'FF-FF'

# === packet types
PKT_TYPE_DATA                               = u'DATA'
PKT_TYPE_FRAG                               = u'FRAG'
PKT_TYPE_JOIN_REQUEST                       = u'JOIN_REQUEST'
PKT_TYPE_JOIN_RESPONSE                      = u'JOIN_RESPONSE'
PKT_TYPE_DIS                                = u'DIS'
PKT_TYPE_DIO                                = u'DIO'
PKT_TYPE_DAO                                = u'DAO'
PKT_TYPE_EB                                 = u'EB'
PKT_TYPE_SIXP                               = u'6P'
PKT_TYPE_KEEP_ALIVE                         = u'KEEP_ALIVE'

# === packet lengths
PKT_LEN_DIS                                 = 8
PKT_LEN_DIO                                 = 76
PKT_LEN_DAO                                 = 20
PKT_LEN_JOIN_REQUEST                        = 20
PKT_LEN_JOIN_RESPONSE                       = 20

# === rpl
RPL_MINHOPRANKINCREASE                      = 256
RPL_PARENT_SWITCH_RANK_THRESHOLD            = 640

RPL_INFINITE_RANK                           = 65535

# === ipv6
IPV6_DEFAULT_HOP_LIMIT                      = 64
IPV6_DEFAULT_PREFIX                         = u'fd00::'
IPV6_ALL_RPL_NODES_ADDRESS                  = u'ff02::1a'

# === sixlowpan
SIXLOWPAN_REASSEMBLY_BUFFER_LIFETIME        = 60 # in seconds
SIXLOWPAN_VRB_TABLE_ENTRY_LIFETIME          = 60 # in seconds

# === sixp
SIXP_MSG_TYPE_REQUEST                       = u'Request'
SIXP_MSG_TYPE_RESPONSE                      = u'Response'
SIXP_MSG_TYPE_CONFIRMATION                  = u'Confirmation'

SIXP_CMD_ADD                                = u'ADD'
SIXP_CMD_DELETE                             = u'DELETE'
SIXP_CMD_RELOCATE                           = u'RELOCATE'
SIXP_CMD_COUNT                              = u'COUNT'
SIXP_CMD_LIST                               = u'LIST'
SIXP_CMD_SIGNAL                             = u'SIGNAL'
SIXP_CMD_CLEAR                              = u'CLEAR'

SIXP_RC_SUCCESS                             = u'RC_SUCCESS'
SIXP_RC_EOL                                 = u'RC_EOL'
SIXP_RC_ERR                                 = u'RC_ERR'
SIXP_RC_RESET                               = u'RC_RESET'
SIXP_RC_ERR_VERSION                         = u'RC_ERR_VERSION'
SIXP_RC_ERR_SFID                            = u'RC_ERR_SFID'
SIXP_RC_ERR_SEQNUM                          = u'RC_ERR_SEQNUM'
SIXP_RC_ERR_CELLLIST                        = u'RC_ERR_CELLLIST'
SIXP_RC_ERR_BUSY                            = u'RC_ERR_BUSY'
SIXP_RC_ERR_LOCKED                          = u'RC_ERR_LOCKED'

SIXP_TRANSACTION_TYPE_2_STEP                = u'2-step transaction'
SIXP_TRANSACTION_TYPE_3_STEP                = u'3-step transaction'

SIXP_TRANSACTION_TYPE_TWO_STEP              = u'two-step transaction'
SIXP_TRANSACTION_TYPE_THREE_STEP            = u'three-step transaction'

SIXP_CALLBACK_EVENT_PACKET_RECEPTION        = u'packet-reception'
SIXP_CALLBACK_EVENT_MAC_ACK_RECEPTION       = u'mac-ack-reception'
SIXP_CALLBACK_EVENT_TIMEOUT                 = u'timeout'
SIXP_CALLBACK_EVENT_FAILURE                 = u'failure'
SIXP_CALLBACK_EVENT_ABORTED                 = u'aborted'

# === sf
MSF_MAX_NUMCELLS                            = 100
MSF_LIM_NUMCELLSUSED_HIGH                   = 0.75 # in [0-1]
MSF_LIM_NUMCELLSUSED_LOW                    = 0.25 # in [0-1]
MSF_HOUSEKEEPINGCOLLISION_PERIOD            = 60   # in seconds
MSF_RELOCATE_PDRTHRES                       = 0.5  # in [0-1]
MSF_MIN_NUM_TX                              = 100  # min number for PDR to be significant

# === tsch
TSCH_MIN_BACKOFF_EXPONENT                   = 1
TSCH_MAX_BACKOFF_EXPONENT                   = 7


# CHANGES HERE REQUIRE CHANGES IN phy_numChans

# https://gist.github.com/twatteyne/2e22ee3c1a802b685695#file-4e_tsch_default_ch-py
TSCH_HOPPING_SEQUENCE_TWO_DOT_FOUR          = [16, 17, 23, 18, 26, 15, 25, 22, 19, 11, 12, 13, 24, 14, 20, 21]



# 868Mhz 250kbps as Brachmann,2014 table II 
#TSCH_HOPPING_SEQUENCE                       = [3, 2, 4, 0, 5, 1, 6]

#868Mhz 1.2kbps as Brachmann,2014 table II
# MR-FSK operating mode #1
# 34 Chann

TSCH_HOPPING_SEQUENCE_EIGHT_SIX_EIGHT       = [11, 10, 32, 9, 16, 20, 4, 23, 25, 6, 18, 14, 24, 15, 19, 26, 5, 7, 29, 12, 17, 22, 27, 13, 8, 21, 3, 31, 28, 30, 33, 0, 2, 1]



#2.4Ghz?
TSCH_MAX_EB_DELAY                           = 180

#868Mhz Change EB max delay to consider lower rate
# TSCH_MAX_EB_DELAY                           = 180*5

TSCH_NUM_NEIGHBORS_TO_WAIT                  = 2
TSCH_DESYNCHRONIZED_TIMEOUT_SLOTS           = 1750
CELLOPTION_TX                               = u'TX'
CELLOPTION_RX                               = u'RX'
CELLOPTION_SHARED                           = u'SHARED'
LINKTYPE_ADVERTISING                        = u'ADVERTISING'
LINKTYPE_ADVERTISING_ONLY                   = u'ADVERTISING_ONLY'
LINKTYPE_NORMAL                             = u'NORMAL'
INTRASLOTORDER_STARTSLOT                    = 0
INTRASLOTORDER_PROPAGATE                    = 1
INTRASLOTORDER_STACKTASKS                   = 2
INTRASLOTORDER_ADMINTASKS                   = 3

# === radio
RADIO_STATE_TX                              = u'tx'
RADIO_STATE_RX                              = u'rx'
RADIO_STATE_OFF                             = u'off'





##################### CHANGE WITH BAND CONFIG #####################

# TWO_DOT_FOUR_GHZ = 0

# EIGHT_SIX_EIGHT_MHZ = 1
# SimConfig.SimConfig._band == '2_4Ghz'

BAND = 1

if not BAND:

	TSCH_HOPPING_SEQUENCE = TSCH_HOPPING_SEQUENCE_TWO_DOT_FOUR

else:

	TSCH_HOPPING_SEQUENCE = TSCH_HOPPING_SEQUENCE_EIGHT_SIX_EIGHT


##################### CHANGE WITH BAND CONFIG #####################

# todo

#consumption for the WHOLE slot
# OpenMote - CC2538
# tx_data = 4ms ( 127 * 8 / 250k)
# tx_ack = 1ms (32 * 8 / 250k)
# slot length 10ms
# CC2538 data: 
# Tx consumption = 24mA at 0dBm, 34mA at 7dBm
# Rx consumption = 20mA at -50dBm, 24mA at -100dBm
# CPU consumption:
# 13mA when ON
# 1.5mA when Tx or RX ( This has to be added to Tx/Rx consumption)
# From: Vilajosana Xavier, Tuset Pere, Watteyne Thomas, Pister Kris. OpenMote: Open-Source Prototyping Platform for the Industrial IoT. In: :211–222EAI;
#2015; San Remo, Italy

# === battery
# Idle: Time slot during which a node listens for data, but receives
# none
CHARGE_IdleListen_uC                        = 6.4
# TxDataRxAck: A timeslot during which the node sends some data frame,
# and expects an acknowledgment (ACK)
CHARGE_TxDataRxAck_uC                       = 54.5
# TxData: Similar to TxDataRxAck, but no ACK is expected. This is
# typically used when the data packet is broadcast
CHARGE_TxData_uC                            = 49.5
# RxDataTxAck: A timeslot during which the node receives some data
# frame, and sends back an ACK to indicate successful reception
CHARGE_RxDataTxAck_uC                       = 32.6
# RxData: Similar to the RxDataTxAck but no ACK is sent (for a
# broadcast packet)
CHARGE_RxData_uC                            = 22.6
# Time slot during which the node’s radio stays off
CHARGE_Sleep_uC                             = 0.0

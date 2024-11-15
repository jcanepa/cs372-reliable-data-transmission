from segment import Segment

class RDTLayer(object):
    """
    The reliable data transfer (RDT) layer is used as a communication
    layer to resolve issues over an unreliable channel.
    """

    DATA_LENGTH = 4  # characters                     # length of string data sent per packet
    FLOW_CONTROL_WIN_SIZE = 15  # characters          # receive window size for flow-control

    send_channel = None                               # channel used for sending data
    receive_channel = None                            # channel used for receiving data
    data_to_send = ''                                 # data to transmit
    count_segment_timeouts = 0                        # total segment timeouts
    timeouts: int                                     # current segment timeouts
    data_sent_count: int                              # number of characters transmitted
    sequence_number: int                              # current sequence number
    ack_number: int                                   # current acknowledgement number
    cumulative_ack: int                               # cumulative acknowledgement
    flow_control: int                                 # verifies pipelined segments fit within flow-control window
    packet_number: int                                # current packets in pipeline
    is_server: bool                                   # type of application: client (default) or server
    payloads: list                                    # uncorrupted payloads
    valid_packets: list                               # packets successfully received by the server
    cached_sequences: list                            # sequence numbers successfully received by the server
    cached_sequence_numbers: list                     # sequence numbers successfully received by the server used to avoid duplication
    uncorrupted_segments: list                        # uncorrupted segments received by the server

    def __init__(self):
        self.send_channel = None
        self.receive_channel = None
        self.data_to_send = ''
        self.count_segment_timeouts = 0
        self.timeouts = 0
        self.data_sent_count = 0
        self.sequence_number = 1
        self.ack_number = 1
        self.cumulative_ack = 1
        self.flow_control = 0
        self.packet_number = 0
        self.is_server = False
        self.payloads = []
        self.valid_packets = []
        self.cached_sequences = []
        self.cached_sequence_numbers = []
        self.uncorrupted_segments = []

    def setSendChannel(self, channel):
        """
        Called by main to set the unreliable sending lower-layer channel
        """
        self.send_channel = channel

    def setReceiveChannel(self, channel):
        """
        Called by main to set the unreliable receiving lower-layer channel
        """
        self.receive_channel = channel

    def setDataToSend(self, data):
        """
        Called by main to set the string data to send
        """
        self.data_to_send = data

    def getDataReceived(self):
        """
        Called by main to get the currently received and buffered string data, in order
        """
        print('getDataReceived(): Complete this...')
        return ""

    def processData(self):
        """
        "timeslice" called by main once per iteration
        """
        self.count_segment_timeouts += 1
        self.processSend()
        self.processReceiveAndSendRespond()

    def processSend(self):
        """
        Manages Segment sending tasks
        """
        # Pipeline segments to fit the flow-control window
        # The flow-control window is the constant RDTLayer.FLOW_CONTROL_WIN_SIZE
        # The maximum data that you can send in a segment is RDTLayer.DATA_LENGTH

        # Somewhere in here you will be creating data segments to send.
        # The data is just part of the entire string that you are trying to send.
        # The seqnum is the sequence number for the segment (in character number, not bytes)

        # deturmine which side of the server/client relationship we are currently dealing with
        if (self.data_to_send == ''):
            self.server = True
            return

        if (self.is_server is True):
            return

        #

        segment_send = Segment()
        seqnum = "0"
        data = "x"

        # Display sending segment
        segment_send.setData(seqnum, data)
        print("Sending segment: ", segment_send.to_string())

        # Use the unreliable send channel to send the segment
        self.send_channel.send(segment_send)

    def processReceiveAndSendRespond(self):
        """
        Manages Segment receive tasks
        """
        segment_ack = Segment()  # segment acknowledging packet(s) received

        # This call returns a list of incoming segments (see Segment class)...
        list_incoming_segments = self.receive_channel.receive()

        # ############################################################################################################ #
        # What segments have been received?
        # How will you get them back in order?
        # This is where a majority of your logic will be implemented
        print('processReceive(): Complete this...')

        # ############################################################################################################ #
        # How do you respond to what you have received?
        # How can you tell data segments apart from ack segments?
        print('processReceive(): Complete this...')

        # Somewhere in here you will be setting the contents of the ack segments to send.
        # The goal is to employ cumulative ack, just like TCP does...
        acknum = "0"

        # ############################################################################################################ #
        # Display response segment
        segment_ack.setAck(acknum)
        print("Sending ack: ", segment_ack.to_string())

        # Use the unreliable send channel to send the ack packet
        self.send_channel.send(segment_ack)
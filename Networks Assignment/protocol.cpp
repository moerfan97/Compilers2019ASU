#include"protocol.h"
#include"ctime"
#include"iostream"

using namespace std;
packet data_packet[8] = { {'o','m','a','r'},
					{'m','o','h','d'},
					{'e','r','f','n'},
					{'s','w','a','t'},
					{'x','m','a','r'},
					{'k','m','n','r'} ,
					{'e','r','f','n'},
					{'s','w','a','t'}
};
bool flag_receive=false;
float ack_return[8] = {0,0,0,0,0,0,0,0};
packet recieved;
frame switch_to_and_from_physical;
clock_t start;
double duration;
event_type event;
/* wait for an event to happen; return its type of event */
void wait_for_event(event_type* event)
{
	int x = *event;
	while (1)
	{
		if (x >= 0 && x <= 3)
		{
			break;
		}
	}
}

/* fetch a packet from the network layer for transmission */
void from_network_layer(packet* p,seq_nr next_frame)
{
	*p = data_packet[next_frame];
}

/* deliver information from an inbound frame to the network layer */
void to_network_layer(packet* p)
{
	recieved = *p;

}

/* get an inbound frame from the physical layer */
void from_physical_layer(frame* r,seq_nr frame_nr)
{
	ack_return[frame_nr] = (frame_nr+3)%7;///transmission+from physical to network
	*r = switch_to_and_from_physical;
}

/* pass the frame to the physical layer */
void to_physical_layer(frame* s)
{
	switch_to_and_from_physical = *s;
}

/* start the clock and enable the timeout event */
void start_timer(seq_nr k)
{
	start = clock();
}

/* stop the clock and disable the timeout event */
void stop_timer(seq_nr k)
{
	start = 0;
}

/* start an auxiliary timer and enable the ack_timeout event 
void start_ack_timer(seq_nr k);

/* stop an auxiliary timer and disable the ack_timeout event 
void stop_ack_timer(seq_nr k);*/

/* allow the network to cause a network_layer_ready event */
void enable_network_layer(void)
{
	if (!flag_receive)
	{
		event = network_layer_ready;
	}
	else
	{
		event = frame_arrival;
	}
}

/* forbid the network to cause a network_layer_ready event */
void disable_network_layer(void)
{
	event = network_layer_ready;
}

///
static bool between(seq_nr a, seq_nr b, seq_nr c)
{
	/* Return true if a <= b < c circularly; false otherwise. */
	if (((a <= b) && (b < c)) || ((c < a) && (a <= b)) || ((b < c) && (c < a)))
		return(true);
	else
		return(false);
}
static void send_data(seq_nr frame_nr, seq_nr frame_expected, packet buffer[])
{
	/* Construct and send a data frame. */
	frame s; /* scratch variable */
	s.info = buffer[frame_nr]; /* insert packet into frame */
	s.seq = frame_nr; /* insert sequence number into frame */
	s.ack = (frame_expected + MAX_SEQ) % (MAX_SEQ + 1); /* piggyback ack */
	to_physical_layer(&s); /* transmit the frame */
	flag_receive = true;
	start_timer(frame_nr); /* start the timer running */
}
void protocol5(void)
{
	seq_nr next_frame_to_send; /* MAX SEQ > 1; used for outbound stream */
	seq_nr ack_expected; /* oldest frame as yet unacknowledged */
	seq_nr frame_expected; /* next frame expected on inbound stream */
	frame r; /* scratch variable */
	packet buffer[MAX_SEQ + 1]; /* buffers for the outbound stream */
	seq_nr nbuffered; /* number of output buffers currently in use */
	seq_nr i; /* used to index into the buffer array */
	//event_type event;

	enable_network_layer(); /* allow network_layer_ready events */
	ack_expected = 0; /* next ack expected inbound */
	next_frame_to_send = 0; /* next frame going out */
	frame_expected = 0; /* number of frame expected inbound */
	nbuffered = 0; /* initially no packets are buffered */


	while (true) {
		wait_for_event(&event); /* four possibilities: see event type above */
		switch (event) {
			case network_layer_ready : /* the network layer has a packet to send */
			/* Accept, save, and transmit a new frame. */
				from_network_layer(&buffer[next_frame_to_send],next_frame_to_send); /* fetch new packet */
				nbuffered = nbuffered + 1; /* expand the sender’s window */
				send_data(next_frame_to_send, frame_expected, buffer);/* transmit the frame */
				cout << "data " << nbuffered << " sent..." << endl;
				inc(next_frame_to_send); /* advance sender’s upper window edge */
				break;

			case frame_arrival : /* a data or control frame has arrived */
				cout << "frame " << nbuffered << " arrived.." << endl;
					from_physical_layer(&r,(next_frame_to_send)-1); /* get incoming frame from physical layer */
					if (r.seq == frame_expected) {
						/* Frames are accepted only in order. */
						to_network_layer(&r.info); /* pass packet to network layer */
						cout << "packet " << nbuffered << " to network..." << endl;
						flag_receive = false;
						
						inc(frame_expected); /* advance lower edge of receiver’s window */
					}
					/* Ack n implies n − 1, n − 2, etc. Check for this. */
					while (between(ack_expected, r.ack, next_frame_to_send)) {
						/* Handle piggybacked ack. */
						nbuffered = nbuffered - 1; /* one frame fewer buffered */
						stop_timer(ack_expected); /* frame arrived intact; stop timer */
						inc(ack_expected); /* contract sender’s window */
					}
					break;

			case cksum_err : break; /* just ignore bad frames */

			case timeout: /* trouble; retransmit all outstanding frames */
						next_frame_to_send = ack_expected; /* start retransmitting here */
						cout << "timeout " << nbuffered << " happened" << endl;
						for (i = 1; i <= nbuffered; i++) {
							send_data(next_frame_to_send, frame_expected, buffer);/* resend frame */
							inc(next_frame_to_send); /* prepare to send the next one */
						}
		}
		if (start > 0)
		{
			duration = (clock() - start) / (double)CLOCKS_PER_SEC;
			if (duration > 100)
			{
				event = timeout;
			}
			else
			{

			}
		}
		else
		{

		}
		if (nbuffered < MAX_SEQ)
			enable_network_layer();
		else
			disable_network_layer();
	}
}


int main() {
	
	protocol5();
	return 0;
}



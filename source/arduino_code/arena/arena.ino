
#include "PixyUART.h"

const int waitFrames = 50;		// check for blocks every waitFrames frames (Pixy runs at 50 fps)
const int reportFrames = 50;	// send report every reportFrames frames (Pixy runs at 50 fps)
const int numCameras = 1;
const int numObjs = 7;
const int bufSize = 32;
const int bigBufSize = 512;

PixyUART pixy;

struct object {
	int x;
	int y;
	int width;
	int height;
	int angle;
	int multiple;
	int updated;
};

struct camera {
	object objects[numObjs];
};

camera cameras[numCameras];

void setup() {
	Serial.begin(9600);
	Serial.print("Starting\n");

	pixy.init();
	initialize();
}

void loop() {
	static int i = 0;
	int j;
	uint16_t blocks;
	char buf[bufSize];

	blocks = pixy.getBlocks();
	i++;

	if(i % waitFrames == 0) {
		if (blocks) {
			// sprintf(buf, "Detected %d blocks\n", blocks);
			// Serial.print(buf);
			if (updateData(0, blocks)) {
				// sprintf(buf, "Update completed, detected %d blocks\n", blocks);
				// Serial.print(buf);
			} else {
				// Serial.print("Error updating data\n");
			}
			// for (int j = 0; j < numCameras; j++) {
			// 	if (!updateData(j, blocks)) {
			// 		Serial.print("Error updating camera " + j + "\n");
			// 	}
			// }
		} else {
			// Serial.print("No blocks detected\n");
		}
	}

	if (i % reportFrames == 0) {
		delay(1000);
		char buff[bigBufSize];
		sprintf(buff, report());
		Serial.print(buff);
	}
}

/*
	Initializes camera object data to zeros
*/
int initialize() {
	for (int i = 0; i < numCameras; i++) {
		for (int j = 0; j < numObjs; j++) {
			cameras[i].objects[j] = {0, 0, 0, 0, 0, 0};
		}
	}
	return 1;
}

/*
	Updates the camera object data with the blocks returned from the pixy
	Returns 1 if update was successful, 0 if update failed
*/
int updateData(int cam, uint16_t blocks) {
	// check if cam is a valid camera id
	if(cam >= numCameras) {
		return 0;
	}

	// clear the multiple flags
	for (int i = 0; i < numObjs; i++) {
		cameras[cam].objects[i].multiple = 0;
	}

	for (int j = 0; j < blocks; j++) {
		// if the returned signature is more than the number of objects a camera can track, then there is a (probably config) problem
		if(pixy.blocks[j].signature >= numObjs) {
			return 0;
		}
		if (!cameras[cam].objects[pixy.blocks[j].signature - 1].updated) {
			object o;
			o.x = pixy.blocks[j].x;
			o.y = pixy.blocks[j].y;
			o.width = pixy.blocks[j].width;
			o.height = pixy.blocks[j].height;
			o.angle = pixy.blocks[j].angle;
			o.updated = 1;
			cameras[cam].objects[pixy.blocks[j].signature - 1] = o;
		} else {
			cameras[cam].objects[pixy.blocks[j].signature - 1].multiple = 1;
		}
	}

	// clear the updated flags for this update
	for (int i = 0; i < numObjs; i++) {
		cameras[cam].objects[i].updated = 0;
	}
	return 1;
}

/*
	Returns an output string representing a JSON object containing all of the camera object data. Also reinitializes the stored data.
*/
char* report() {
	char output[bigBufSize] = "\"{\n";
	for (int i = 0; i < numCameras; i++) {
		for (int j = 0; j < numObjs; j++) {
			char buff[bufSize];
			object o = cameras[i].objects[j];
			sprintf(buff, "\"C%dO%d\":\"[%d, %d, %d, %d, %d, %d]\"", i+1, j+1, o.x, o.y, o.width, o.height, o.angle, o.multiple);
			strcat(output, buff);
			if (j == numObjs - 1) {
				strcat(output, "\n");
			} else {
				strcat(output, ",\n");
			}
		}
	}
	strcat(output, "}\"\n");
	// reinitialize data
	initialize();
	return output;
}

// void handleInput (int cmd) {
// 	switch (cmd) {
// 		case 1:
// 			char buff[bigBufSize];
// 			sprintf(buff, report());
// 			Serial.println(buff);
// 			break;
// 		default:
// 			Serial.println("Unsupported command: " + String(cmd));
// 	}
// }

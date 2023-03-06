import { BoardPhotoStatus } from './BoardPhotoStatus';

export class Photo {
	boardAddDate: Date;

	constructor(public photoKey: string,
				public s3BucketName: string,
				public s3ObjectKey: string,
				public uploaderCognitoUsername: string,
				public url: string,
				public boardPhotoStatus: BoardPhotoStatus,
				boardAddDateTimestamp: number) {
		this.boardAddDate = new Date(boardAddDateTimestamp);
	}

	static fromWire(wire) {
		return new Photo(wire.photoKey,
		                 wire.s3BucketName,
		                 wire.s3ObjectKey,
		                 wire.uploaderCognitoUsername,
		                 wire.url,
		                 wire.boardPhotoStatus,
						 wire.boardAddDateTimestamp);
	}
}
import { Injectable } from '@angular/core';

import { UploadUrlService } from '../services/upload-url.service';
import { PhotoWebsocketService } from '../services/photo-websocket.service';
import { BoardService } from '../services/board.service';

import { Photo } from '../dtos/Photo';
import { Board } from '../dtos/Board';
import { BoardPhotoStatus } from '../dtos/BoardPhotoStatus';

@Injectable({
	providedIn: 'root'
})
export class PhotoCanvasService {
	public activePhotos: Photo[] = [];
	public connectionActive: boolean = false;

	readonly idleTimeoutLength: number = 30 * 1000; /* 30 seconds */
	readonly maxActivePhotos: number = 20;
	readonly minExtraPhotosToEnableCycling: number = 10;

	private board: Board;
	private idleTimer: ReturnType<typeof setTimeout>;
	private allActivePhotoKeys: string[] = [];
	private nextInactivePhotoIndex = 0;
	private onDisconnectCallback: () => void;
	private onReconnectCallback: () => void;


	constructor(private uploadUrlService: UploadUrlService,
				private photoWebsocketService: PhotoWebsocketService,
				private boardService: BoardService) { }


	initialize(board: Board) {
		this.board = board;

		this.getAllActivePhotoKeys();
		this.connectToWebsocket();
		this.resetIdleTimer();

		return this.getActivePhotoUrls();
	}

	setTriggers(onDisconnect, onReconnect) {
		this.onDisconnectCallback = onDisconnect;
		this.onReconnectCallback = onReconnect;
	}

	teardown() {
		this.photoWebsocketService.disconnect();
	}

	private handleMessage(message) {
		console.log(message);
		let event = JSON.parse(message.data);
		switch (event.action) {
			case 'newPhotos':
				this.handleNewPhotoFromWebsocket(event);
				break;
			case 'removePhotos':
				this.handleRemovePhotos(event);
			case 'ping':
				break;
			default:
				console.error('Unexpected websocket message: ' + event.action);
		}
	}

	private handleError(error) {
		// TODO(sgoldstein)
		console.error(error);
	}

	private handleDisconnect() {
		console.log('Websocket disconnected. Reconnecting...');
		this.connectToWebsocket();
		if (this.onDisconnectCallback) {
			this.onDisconnectCallback();
		}
	}

	private handleNewPhotoFromWebsocket(event) {
		console.log('New photo(s).');
		let newPhotos = event.photos.map(photo => Photo.fromWire(photo));
		this.allActivePhotoKeys.push(newPhotos.map(photo => photo.photoKey));

		this.activePhotos = this.activePhotos.concat(newPhotos);

		this.trimExcessActivePhotos();
		this.resetIdleTimer();
	}

	private handleRemovePhotos(event) {
		console.log('Photo(s) removed.');
		this.allActivePhotoKeys = this.allActivePhotoKeys.filter(photoKey => !event.photoKeys.includes(photoKey));
		this.activePhotos = this.activePhotos.filter(photo => !event.photoKeys.includes(photo.photoKey));
	}

	private connectToWebsocket() {
		this.photoWebsocketService.connect(this.board.joinCode)
		.then(subj => {
			console.log('WebSocket connection successful.');
			if (this.onReconnectCallback) {
				this.onReconnectCallback();
			}
			subj.subscribe(msg => this.handleMessage(msg),
			               err => this.handleError(err),
			               () => this.handleDisconnect());
		})
		.catch(err => {
			console.error('WebSocket connection failed:');
			console.error(err);
			console.error('Will retry shortly.');
			setTimeout(() => this.connectToWebsocket(), 5000);
		});
	}

	private slowLoadPhotoForTesting(numPhotos: number) {
		let photo = new Photo("photoKey", "bucketName", "objectKey", "username", "assets/ballz.jpg", BoardPhotoStatus.Active, 123456789);
		setTimeout(() => {
			if (this.activePhotos.length < numPhotos) {
				this.activePhotos = this.activePhotos.concat(photo);
				this.slowLoadPhotoForTesting(numPhotos);
			}
		}, 125);
	}

	private getActivePhotoUrls() {
		return this.uploadUrlService.getPhotoUrls(this.board.joinCode)
		.then(result => {
			result = result as Photo[];
			result.sort((a, b) => {
				return a.boardAddDate.valueOf() - b.boardAddDate.valueOf();
			});
			this.activePhotos = result;
			this.trimExcessActivePhotos();
		})
		.catch(error => {
			console.error(error);
		});
	}

	private trimExcessActivePhotos() {
		while (this.activePhotos.length > this.maxActivePhotos) {
			this.activePhotos.shift();
		}
	}

	private getAllActivePhotoKeys() {
		this.boardService.getAllPhotoCodes(this.board.joinCode)
		.then(result => {
			this.allActivePhotoKeys = result;
		})
		.catch(error => {
			console.error(error);
		})
	}

	private addNextInactivePhoto(): void {
		if (this.allActivePhotoKeys.length - this.activePhotos.length <= this.minExtraPhotosToEnableCycling) {
			// Not enough photos to enable cycling; return
			return;
		}

		this.findNextInactivePhotoToAdd(3)
		.then(result => {
			if (result) {
				this.activePhotos.push(result);
			}
		})
		.catch(err => {
			console.log(err);
		})
		.finally(() => {
			this.resetIdleTimer();
			this.trimExcessActivePhotos();
		});
	}

	private findNextInactivePhotoToAdd(maxAttempts: number) {
		// Finds next inactive photo that could be added (no restrictions on it & not on board)
		// If maxAttempts photos all fail, no photos will be added this time and a void promise will return
		if (maxAttempts < 1) {
			return Promise.resolve(null);
		}
		let currentInactivePhotoIndex = this.nextInactivePhotoIndex;
		this.advanceNextInactivePhotoIndex();

		let nextPhotoKey = this.allActivePhotoKeys[currentInactivePhotoIndex];
		let photoAlreadyOnBoard = this.activePhotos.findIndex(p => p.photoKey == nextPhotoKey) > -1;
		if (photoAlreadyOnBoard) {
			return this.findNextInactivePhotoToAdd(maxAttempts - 1);
		}

		return this.uploadUrlService.getPhotoUrlsByPhotoKeys(this.board.joinCode, [nextPhotoKey])
		.then(response => {
			response = response as Photo[];
			if (response.length > 1) {
				throw Error('Expected only one photo to be returned by API.');
			}
			else if (response.length < 1) {
				return this.findNextInactivePhotoToAdd(maxAttempts - 1);
			}
			else {
				let newPhoto = response[0];

				// Remove from list of active photos if photo is no longer active
				if (newPhoto.boardPhotoStatus != BoardPhotoStatus.Active) {
					let photoIndex = this.allActivePhotoKeys.indexOf(newPhoto.photoKey);
					if (photoIndex > -1) {
						this.allActivePhotoKeys.splice(photoIndex, 1);
					}

					return this.findNextInactivePhotoToAdd(maxAttempts - 1);
				} else {
					return newPhoto;
				}
			}
		});
	}

	private advanceNextInactivePhotoIndex() {
		this.nextInactivePhotoIndex++;
		if (this.nextInactivePhotoIndex >= this.allActivePhotoKeys.length) {
			this.nextInactivePhotoIndex = 0;
		}
	}

	private resetIdleTimer() {
		this.idleTimer = setTimeout(() => {
			this.addNextInactivePhoto();
		}, this.idleTimeoutLength);
	}
}

import { Injectable } from '@angular/core';
import { API } from 'aws-amplify';

import { BaseService } from './base-service';
import { Photo } from '../dtos/Photo';
import { BoardPhotoStatus } from '../dtos/BoardPhotoStatus';

@Injectable({
	providedIn: 'root'
})
export class UploadUrlService extends BaseService {
	private apiName = 'BoardAPI';

	async uploadFile(file: File, boardJoinCode: string) {
		return this.getUploadUrl(file, boardJoinCode)
		.then(getUrlResponse => {
			return this.uploadFileWithRequest(file, getUrlResponse)
			.then(_ => {
				// Info about photo for app db is returned by uploadURL;
				// use this to add photo to board
				return {
					photoKey: getUrlResponse.photoKey,
					s3BucketName: getUrlResponse.s3BucketName,
					s3ObjectKey: getUrlResponse.s3ObjectKey,
					boardJoinCode: boardJoinCode
				};
			});
		})
		.then(params => {
			return this.addPhotoToBoard(params);
		});
	}

	async getPhotoUrls(boardJoinCode: string,
	                   photoStatuses: BoardPhotoStatus[] = [BoardPhotoStatus.Active],
	                   beforeDate: Date = new Date(),
	                   pageNumber: number = 0,
	                   pageSize: number = 50): Promise<Photo[]> {
		const path = '/presigned-urls';
		const init = await super.getInit();


		init.queryStringParameters = {
			'join-code': boardJoinCode,
			'page-number': pageNumber,
			'page-size': pageSize,
			'before-date': beforeDate.toISOString(),
			'photo-status': photoStatuses
		};

		return API.get(this.apiName, path, init)
			.then(response => {
				return response.photos.map(Photo.fromWire);
			});
	}

	async getPhotoUrlsByPhotoKeys(boardJoinCode: string, photoKeys: string[]): Promise<Photo[]> {
		const path = '/presigned-urls';
		const init = await super.getInit();

		init.queryStringParameters = {
			'join-code': boardJoinCode,
			'photo-key': photoKeys
		}

		return API.get(this.apiName, path, init)
		.then(result => {
			return result.photos.map(Photo.fromWire);
		})
	}

	private async getUploadUrl(file: File, boardJoinCode: string) {
		const presignedUrlPath = '/public/presigned-urls';

		const init = await super.getInit();
		init.body = {
			fileExtension: this.getFileExtension(file),
			joinCode: boardJoinCode
		};

		return API.post(this.apiName, presignedUrlPath, init);
	}

	private async uploadFileWithRequest(file: File, presignedPostData) {
		const formData = new FormData();
		Object.keys(presignedPostData.fields).forEach(key => {
			formData.append(key, presignedPostData.fields[key]);
		})

		formData.append('file', file);

		return fetch(presignedPostData.url, {
			method: 'POST',
			body: formData
		});
	}

	private async addPhotoToBoard(params) {
		const boardPhotoPath = `/public/boards/${params.boardJoinCode}/photos`;

		const init = await super.getInit();
		init.body = {
			photoKey: params.photoKey,
			s3BucketName: params.s3BucketName,
			s3ObjectKey: params.s3ObjectKey
		};

		return API.post(this.apiName, boardPhotoPath, init);
	}

	private getFileExtension(file: File) {
		return file.name.split('.').pop();
	}
}

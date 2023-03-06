import { Injectable } from '@angular/core';
import { API } from 'aws-amplify';

import { BaseService } from './base-service';
import { Board } from '../dtos/Board';
import { BoardStatus } from '../dtos/BoardStatus';
import { BoardPhotoStatus } from '../dtos/BoardPhotoStatus';
import { BoardToCreate } from '../dtos/BoardToCreate';

@Injectable({
	providedIn: 'root'
})
export class BoardService extends BaseService {
	private apiName = 'BoardAPI';
	private authenticatedPath = '/boards';
	private unauthenticatedPath = '/public/boards';

	async getBoardByJoinCode(joinCode: string): Promise<Board> {
		const init = await super.getInit();
		let pathWithArgs = this.unauthenticatedPath + `?joinCode=${joinCode}`

		return API
		.get(this.apiName, pathWithArgs, init)
		.then(result => {
			return Board.fromWire(result);
		});
	}

	async getAllPhotoCodes(joinCode: string): Promise<string[]> {
		const init = await super.getInit();
		let path = `${this.authenticatedPath}/${joinCode}/photos`;

		return API
		.get(this.apiName, path, init)
		.then(result => {
			return result.photoKeys;
		})
	}

	async getBoards(): Promise<Board[]> {
		const init = await super.getInit();

		return API
		.get(this.apiName, this.authenticatedPath, init)
		.then(boards => {
			return boards.map(Board.fromWire);
		});
	}

	async createBoard(boardToCreate: BoardToCreate): Promise<Board> {
		const init = await super.getInit();
		init.body = boardToCreate;

		return API
		.post(this.apiName, this.authenticatedPath, init);
	}

	async updateBoard(joinCode: string, boardStatus: BoardStatus): Promise<Board> {
		const init = await super.getInit();
		let path = `${this.authenticatedPath}/${joinCode}`;
		init.body = {
			'boardStatus': boardStatus
		};

		return API
		.put(this.apiName, path, init)
		.then(result => {
			return Board.fromWire(result);
		});
	}

	async updateBoardPhoto(joinCode: string, photoKey: string, newStatus: BoardPhotoStatus): Promise<void> {
		const init = await super.getInit();
		let path = `${this.authenticatedPath}/${joinCode}/photos`;

		init.body = {
			'photoKey': photoKey,
			'boardPhotoStatus': newStatus
		}

		return API
		.put(this.apiName, path, init);
	}

	async startBoard(joinCode: string): Promise<Board> {
		return this.updateBoard(joinCode, BoardStatus.Active);
	}
}

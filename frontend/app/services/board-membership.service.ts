import { Injectable } from '@angular/core';
import { API } from 'aws-amplify';

import { BaseService } from './base-service';
import { BoardMembership } from '../dtos/BoardMembership';
import { BoardMembershipStatus } from '../dtos/BoardMembershipStatus';

@Injectable({
	providedIn: 'root'
})
export class BoardMembershipService extends BaseService {
	private apiName = 'BoardAPI';
	private path = '/board-memberships';

	async getBoardMemberships(): Promise<BoardMembership[]> {
		const init = await super.getInit();

		return API
		.get(this.apiName, this.path, init)
		.then(response => {
			return response.map(BoardMembership.fromWire);
		});
	}

	async joinBoard(joinCode: string): Promise<any> {
		const init = await super.getInit();

		init.body = {
			joinCode: joinCode,
			boardMembershipStatus: BoardMembershipStatus.Active
		}
		return API
		.post(this.apiName, this.path, init);
	}
}

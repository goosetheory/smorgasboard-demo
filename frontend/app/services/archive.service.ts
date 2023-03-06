import { Injectable } from '@angular/core';
import { API } from 'aws-amplify';

import { BaseService } from './base-service';
import { Archive } from '../dtos/Archive';

@Injectable({
  providedIn: 'root'
})
export class ArchiveService extends BaseService {
	private apiName = 'BoardAPI';
	private authenticatedPath = '/archives';


	async getArchiveByJoinCode(joinCode: string): Promise<Archive> {
		const init = await super.getInit();
		let pathWithArgs = this.authenticatedPath + `?joinCode=${joinCode}`;

		return API
		.get(this.apiName, pathWithArgs, init);
	}
}

import { Auth } from 'aws-amplify';

export class BaseService {
	protected async getInit(): Promise<any> {
		return await Auth.currentSession()
		.then(session => {
			return {
				headers: {
					Authorization: `Bearer ${session.getIdToken().getJwtToken()}`
				}
			};
		})
		.catch(err => {
			return {};
		});
	}
}
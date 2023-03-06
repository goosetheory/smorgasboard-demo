import { BoardMembershipStatus } from './BoardMembershipStatus';

export class BoardMembership {
	joinDate: Date;

	constructor(public boardName: string,
				public joinCode: string,
				public cognitoUsername: string,
				public givenName: string,
				public status: BoardMembershipStatus,
				joinDateInt: number) {
		this.joinDate = new Date(joinDateInt);
	}

	static fromWire(wire) {
		return new BoardMembership(wire.boardName,
								   wire.joinCode,
								   wire.cognitoUsername,
								   wire.givenName,
								   wire.status,
								   wire.joinDate);
	}
}
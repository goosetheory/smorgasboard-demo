import { BoardStatus } from './BoardStatus';
import { BoardType } from './BoardType';

export class Board {
	startDate: Date;
	endDate: Date;

	constructor(public boardName: string,
				public joinCode: string,
				public boardStatus: BoardStatus,
				public boardType: BoardType,
				startDateTimestamp: number,
				endDateTimestamp: number) {
		this.startDate = new Date(startDateTimestamp);
		this.endDate = new Date(endDateTimestamp);
	}

	static fromWire(wire) {
		return new Board(wire.boardName,
		                 wire.joinCode,
		                 wire.boardStatus,
		                 wire.boardType,
		                 wire.startDateTimestamp,
		                 wire.endDateTimestamp);
	}
}
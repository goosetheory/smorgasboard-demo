import { Component, OnInit, Input } from '@angular/core';


import { Board } from '../../dtos/Board';
import { BoardType } from '../../dtos/BoardType';
@Component({
	selector: 'app-board-trial-info',
	templateUrl: './board-trial-info.component.html',
	styleUrls: ['./board-trial-info.component.scss']
})
export class BoardTrialInfoComponent implements OnInit {
	@Input() board: Board;

	constructor() { }

	ngOnInit(): void {
	}

	isFreeTrial(): boolean {
		return this.board.boardType == BoardType.FreeTrial;
	}
}

import { Component, Input, OnInit, ViewChild, ElementRef } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

import { Board } from '../dtos/Board';
import { BoardType } from '../dtos/BoardType';

@Component({
	selector: 'app-board-created-modal',
	templateUrl: './board-created-modal.component.html',
	styleUrls: ['./board-created-modal.component.scss']
})
export class BoardCreatedModalComponent implements OnInit {
	@Input() board: Board;
	@ViewChild('modal') modal: ElementRef;

	constructor(private modalService: NgbModal) { }

	showModal(): Promise<any> {
		return this.modalService.open(this.modal).result;
	}

	isFreeTrial(): boolean {
		return this.board && this.board.boardType == BoardType.FreeTrial;
	}

	ngOnInit(): void {
	}
}

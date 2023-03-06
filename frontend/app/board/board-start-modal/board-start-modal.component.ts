import { Component, OnInit, ViewChild, Input, ElementRef } from '@angular/core';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';


import { Board } from '../../dtos/Board';
import { BoardType } from '../../dtos/BoardType';

@Component({
	selector: 'app-board-start-modal',
	templateUrl: './board-start-modal.component.html',
	styleUrls: ['./board-start-modal.component.scss']
})
export class BoardStartModalComponent implements OnInit {
	@ViewChild('modal') modal: ElementRef;
	@Input() board: Board;

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

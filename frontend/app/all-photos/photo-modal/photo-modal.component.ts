import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';

import { Photo } from '../../dtos/Photo';
import { BoardPhotoStatus } from '../../dtos/BoardPhotoStatus';
import { BoardService } from '../../services/board.service';
import { ToastService } from '../../services/toast.service';

@Component({
	selector: 'app-photo-modal',
	templateUrl: './photo-modal.component.html',
	styleUrls: ['./photo-modal.component.scss']
})
export class PhotoModalComponent implements OnInit {
	@ViewChild('modal') modal: ElementRef | any;
	photo: Photo;
	openModal: NgbModalRef;
	private joinCode: string;

	constructor(private modalService: NgbModal,
	            private boardService: BoardService,
	            private toastService: ToastService,
	            private route: ActivatedRoute) { }

	showModal(photo: Photo): Promise<any> {
		this.photo = photo;
		this.openModal = this.modalService.open(this.modal, { centered: true });
		return this.openModal.result;
	}

	ngOnInit(): void {
		this.joinCode = this.route.snapshot.params.boardID;
	}

	isPhotoActive(): boolean {
		return this.photo.boardPhotoStatus == BoardPhotoStatus.Active;
	}

	removePhoto() {
		this.boardService.updateBoardPhoto(this.joinCode, this.photo.photoKey, BoardPhotoStatus.RemovedByHost)
		.then(result => {
			this.toastService.show('Photo removed.');
			this.openModal.close();
		})
		.catch(result => {
			this.toastService.error('Could not remove photo.');
		});
	}
}

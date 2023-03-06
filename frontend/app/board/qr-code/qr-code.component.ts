import { Input, Component, OnInit } from '@angular/core';
import { AddPhotoLinkService } from '../../services/add-photo-link.service';

@Component({
	selector: 'app-qr-code',
	templateUrl: './qr-code.component.html',
	styleUrls: ['./qr-code.component.scss']
})
export class QrCodeComponent implements OnInit {
	@Input() joinCode: string;
	qrUrl: string;

	constructor(private addPhotoLinkService: AddPhotoLinkService) {
	}

	ngOnInit(): void {
		this.qrUrl = this.addPhotoLinkService.getAddPhotoLink(this.joinCode);
	}
}

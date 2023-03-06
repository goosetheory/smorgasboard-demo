import { Auth } from 'aws-amplify';
import { Injectable } from '@angular/core';
import { Observable, Observer, Subject, of  } from "rxjs";
import { environment } from '../../environments/environment';

@Injectable({
	providedIn: 'root'
})
export class PhotoWebsocketService {
	websocket: WebSocket;
	subject: Subject<MessageEvent>;

	readonly pingFreqMs = 30 * 1000;

	private baseUrl = environment.websocketUrl;
	private pingTimer;

	constructor() { }

	public connect(joinCode): Promise<Subject<MessageEvent>> {
		if (!this.subject || this.websocket.readyState != WebSocket.OPEN) {
			console.log('Websocket connecting...');
			return this.create(this.baseUrl, joinCode);
		} else {
			return Promise.resolve(this.subject);
		}
	}

	public disconnect() {
		if (this.subject) {
			this.subject.complete();
			this.cancelPings();
		}
	}

	public sendMessage(message: any) {
		if (this.websocket.readyState == WebSocket.OPEN) {
			this.websocket.send(JSON.stringify(message));
		} else {
			console.error('Could not send websocket message. Websocket is closed.')
		}
	}

	private async create(baseUrl, joinCode): Promise<Subject<MessageEvent>> {
		return Auth.currentSession()
		.then(currentSession => {
			let jwt = currentSession.getIdToken().getJwtToken();
			let url = `${baseUrl}?authorizer=${jwt}&joinCode=${joinCode}`;
			this.websocket = new WebSocket(url);

			let observable = Observable.create((obs: Observer<MessageEvent>) => {
				this.websocket.onmessage = obs.next.bind(obs);
				this.websocket.onerror = obs.error.bind(obs);
				this.websocket.onclose = obs.complete.bind(obs);
				return this.websocket.close.bind(this.websocket);
			});
			let observer = {
				next: (data: Object) => {
					this.sendMessage(data);
				}
			};
			this.subject = Subject.create(observer, observable);

			return new Promise((resolve, reject) => {
				if (this.websocket.readyState === WebSocket.OPEN) {
					this.schedulePings();
					resolve(this.subject);
				}

				this.websocket.onopen = () => {
					this.schedulePings();
					resolve(this.subject);
				};

				this.websocket.onerror = (err) => reject(err);
			});
		});
	}

	private schedulePings() {
		if (this.pingTimer) {
			return;
		}

		this.pingTimer = setInterval(() => {
			if (this.websocket.readyState == WebSocket.OPEN) {
				this.sendMessage({'action': 'ping'});
			}
		}, this.pingFreqMs);
	}

	private cancelPings() {
		if (!this.pingTimer) {
			return;
		}

		clearInterval(this.pingTimer);
	}
}

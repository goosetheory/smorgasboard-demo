import { BaseService } from './base-service';
import { API } from 'aws-amplify';

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { BlogPost } from '../dtos/BlogPost';

@Injectable({
	providedIn: 'root'
})
export class BlogService extends BaseService {
	private apiName = 'BoardAPI';
	private unauthenticatedPath = '/public/blog-posts';
	private baseUrl: string = 'https://public-api.wordpress.com/rest/v1.1/sites/trysmorgasboard.wordpress.com';

	public async getAllPosts(): Promise<Array<BlogPost>> {
		const init = await super.getInit();
		return API
		.get(this.apiName, this.unauthenticatedPath, init)
		.then(response => {
			return response.posts;
		});
	}

	public async getPost(slug: string): Promise<BlogPost> {
		const init = await super.getInit();
		init.queryStringParameters = {
			'slug': slug
		}

		return API
		.get(this.apiName, this.unauthenticatedPath, init);
	}
}

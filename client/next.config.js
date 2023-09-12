/** @type {import('next').NextConfig} */
require("dotenv").config({ 'path': '../.env' })
module.exports = {
	/*async rewrites() {
		return [
			{
				source: '/api/:path*',
				destination: `http://${process.env.HOST}:${process.env.API_PORT}/api/:path*`,
			},
		]
	},*/
	experimental: {
		serverActions: true
	}
}
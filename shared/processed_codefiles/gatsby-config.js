require("dotenv").config({
path: `.env.${process.env.NODE_ENV}`,
})
module.exports = {
siteMetadata: {
title: `Gatsby Default Starter`,
description: `Kick off your next, great Gatsby project with this default starter. This barebones starter ships with the main Gatsby configuration files you might need.`,
author: `@gatsbyjs`,
},
plugins: [
"gatsby-plugin-emotion",
`gatsby-plugin-react-helmet`,
{
resolve: `gatsby-source-filesystem`,
options: {
name: `images`,
path: `${__dirname}/src/images`,
},
},
`gatsby-transformer-sharp`,
`gatsby-plugin-sharp`,
{
resolve: `gatsby-plugin-manifest`,
options: {
name: `gatsby-starter-default`,
short_name: `starter`,
start_url: `/`,
background_color: `#663399`,
theme_color: `#663399`,
display: `minimal-ui`,
},
},
{
resolve: "gatsby-source-datocms",
options: {
apiToken: process.env.DATO_CMS_API_TOKEN,
},
},
],
}
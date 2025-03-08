# Build Stage
FROM node:20 AS build
WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install --legacy-peer-deps

# Copy source files & build the project
COPY . .
RUN npm run build

# Serve Stage
FROM node:20 AS runtime
WORKDIR /app

# Install a lightweight static file server
RUN npm install -g serve

# Copy built files from the build stage
COPY --from=build /app/dist ./dist

# Expose port and run the server
EXPOSE 3000
CMD ["serve", "-s", "dist", "-l", "3000"]
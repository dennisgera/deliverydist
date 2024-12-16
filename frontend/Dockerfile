FROM node:20-slim

# Set working directory
WORKDIR /app

# Copy frontend dependencies
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend code
COPY . .

# Build frontend
RUN npm run build

# Expose frontend port
EXPOSE 3000

# Command to run frontend
CMD ["npm", "run", "start"]
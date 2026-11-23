# Multi-Stage Dockerfile for DEPA College A Provider (Server 2)
FROM maven:3.9.6-eclipse-temurin-21 AS build
WORKDIR /app

COPY pom.xml .
COPY consent-manager/backend consent-manager/backend
COPY college-a/backend college-a/backend
COPY college-b/backend college-b/backend
RUN mvn clean package -pl college-a/backend -am -DskipTests

FROM eclipse-temurin:21-jre-alpine
WORKDIR /app

ENV PORT=8081 \
    APP_COLLEGE_CODE=COLLEGE_A \
    APP_COLLEGE_NAME="College A University" \
    APP_CM_BASE_URL="http://server1-cm:8095" \
    APP_INTERNAL_API_KEY="A-INTERNAL-SECRET-KEY"

COPY --from=build /app/college-a/backend/target/*.jar app.jar

EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]

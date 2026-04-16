-- CreateTable
CREATE TABLE "Sport" (
    "id" SERIAL NOT NULL,
    "slug" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "Sport_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Team" (
    "id" SERIAL NOT NULL,
    "abbreviation" TEXT NOT NULL,
    "sportId" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "city" TEXT NOT NULL,
    "primaryHex" TEXT NOT NULL,
    "secondaryHex" TEXT NOT NULL,
    "stadiumName" TEXT NOT NULL,
    "stadiumPrompt" TEXT NOT NULL,
    "skylinePrompt" TEXT NOT NULL,
    "skyPrompt" TEXT NOT NULL,
    "jerseyPrompt" TEXT NOT NULL,
    "pantsPrompt" TEXT NOT NULL,
    "helmetPrompt" TEXT NOT NULL,
    "numberStyle" TEXT NOT NULL,
    "logoPrompt" TEXT NOT NULL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Team_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "CardPlayer" (
    "id" SERIAL NOT NULL,
    "teamId" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    "number" TEXT NOT NULL,
    "position" TEXT NOT NULL,
    "side" TEXT NOT NULL,
    "pose" TEXT NOT NULL DEFAULT 'auto',
    "ball" TEXT NOT NULL DEFAULT 'auto',
    "order" INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT "CardPlayer_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Sport_slug_key" ON "Sport"("slug");

-- CreateIndex
CREATE UNIQUE INDEX "Team_sportId_abbreviation_key" ON "Team"("sportId", "abbreviation");

-- AddForeignKey
ALTER TABLE "Team" ADD CONSTRAINT "Team_sportId_fkey" FOREIGN KEY ("sportId") REFERENCES "Sport"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "CardPlayer" ADD CONSTRAINT "CardPlayer_teamId_fkey" FOREIGN KEY ("teamId") REFERENCES "Team"("id") ON DELETE CASCADE ON UPDATE CASCADE;

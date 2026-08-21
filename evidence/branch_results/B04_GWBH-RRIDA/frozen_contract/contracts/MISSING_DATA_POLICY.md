# Missing-data policy

欠測、member不存在、header不明、alias 0件または複数件、support不明、invalid weight、非finite値、zero width、row不足、config不整合はすべて明示的なunresolved reasonとして保存する。

0への置換、別列・別parameter・別event・別mode・別familyへのfallback、pair削除による分母変更は禁止する。22組の凍結分母を維持し、resolved数とunresolved数を併記する。


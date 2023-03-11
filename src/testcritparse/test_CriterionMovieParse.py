import pytest
from bs4 import BeautifulSoup

from critparse import CriterionMovieParse


def test_extract_info4():
    info = ['(“Heads or Tails”)', 'Directed by Guru Dutt • 1954 • India', 'Starring Guru Dutt, Shyama, Jagdish Sethi', 'Guru Dutt blends noir and comedy with delectable results in this tale of Kalu (Dutt), a poor taxi driver in Bombay who finds himself mixed up with two women and organized crime as he attempts to make enough money to marry. O. P. Nayyar’s hugely popular songs helped make this winning mix of humor and suspense one of the first major successes of director-producer Dutt’s career.']
    country, descr, director, stars, year = CriterionMovieParse.extract_info_len4(info)
    assert country == ' India'
    assert descr == 'Guru Dutt blends noir and comedy with delectable results in this tale of Kalu (Dutt), a poor taxi driver in Bombay who finds himself mixed up with two women and organized crime as he attempts to make enough money to marry. O. P. Nayyar’s hugely popular songs helped make this winning mix of humor and suspense one of the first major successes of director-producer Dutt’s career.' + '\n\n' + '(“Heads or Tails”)'
    assert director == 'Directed by Guru Dutt '
    assert stars == 'Starring Guru Dutt, Shyama, Jagdish Sethi'
    assert year == ' 1954 '


def test_extract_info_len3():
    info = ['Directed by Richard Franklin • 1981 •\xa0Australia, United States', 'Starring Stacy Keach, Jamie Lee Curtis, Marion Edward', 'Stacy Keach is Pat Quid, a trucker who plays solitary games to keep his sanity on long hauls through the desolate Australian outback. Jamie Lee Curtis is a free-spirited hitchhiker looking for excitement, with a game of her own. And somewhere up ahead is a maniac in a van whose game may be butchering young women along the highway. But when the killer decides to raise the stakes, Quid’s game becomes personal—and the rules of this road are about to take some deadly turns. Director Richard Franklin packs plenty of Hitchcockian twists and suspense into this sly shocker that ranks among the most surprising thrillers of the 1980s.']
    country, descr, director, stars, year = CriterionMovieParse.extract_info_len3(info)
    assert country == ' Australia, United States'
    assert descr == 'Stacy Keach is Pat Quid, a trucker who plays solitary games to keep his sanity on long hauls through the desolate Australian outback. Jamie Lee Curtis is a free-spirited hitchhiker looking for excitement, with a game of her own. And somewhere up ahead is a maniac in a van whose game may be butchering young women along the highway. But when the killer decides to raise the stakes, Quid’s game becomes personal—and the rules of this road are about to take some deadly turns. Director Richard Franklin packs plenty of Hitchcockian twists and suspense into this sly shocker that ranks among the most surprising thrillers of the 1980s.'
    assert director == 'Directed by Richard Franklin '
    assert stars == 'Starring Stacy Keach, Jamie Lee Curtis, Marion Edward'
    assert year == '1981'


def test_extract_info_len3_2():
    info = ['ANDREI BOLKONSKY', 'Directed by Sergei Bondarchuk • 1966 • Soviet Union', 'At the height of the Cold War, the Soviet film industry set out to prove it could outdo Hollywood with a production that would dazzle the world: a titanic, awe-inspiring adaptation of Tolstoy’s classic tome in which the fates of three souls—the blundering, good-hearted Pierre; the heroically tragic Prince Andrei; and the radiant, tempestuous Natasha—collide amid the tumult of the Napoleonic Wars. Employing a cast of thousands and an array of innovative camera techniques, director Sergei Bondarchuk conjures a sweeping vision of grand balls that glitter with rococo beauty and breathtaking battles that overwhelm with their expressionistic power. As a statement of Soviet cinema’s might, WAR AND PEACE succeeded wildly, garnering the Academy Award for best foreign-language film and setting a new standard for epic moviemaking.']
    country, descr, director, stars, year = CriterionMovieParse.extract_info_len3(info)
    assert country == ' Soviet Union'
    assert descr == 'ANDREI BOLKONSKY' + '\n\n' + 'At the height of the Cold War, the Soviet film industry set out to prove it could outdo Hollywood with a production that would dazzle the world: a titanic, awe-inspiring adaptation of Tolstoy’s classic tome in which the fates of three souls—the blundering, good-hearted Pierre; the heroically tragic Prince Andrei; and the radiant, tempestuous Natasha—collide amid the tumult of the Napoleonic Wars. Employing a cast of thousands and an array of innovative camera techniques, director Sergei Bondarchuk conjures a sweeping vision of grand balls that glitter with rococo beauty and breathtaking battles that overwhelm with their expressionistic power. As a statement of Soviet cinema’s might, WAR AND PEACE succeeded wildly, garnering the Academy Award for best foreign-language film and setting a new standard for epic moviemaking.'
    assert director == 'Directed by Sergei Bondarchuk '
    assert stars == ''
    assert year == '1966'


def test_extract_info_len3_3():
    info =['Directed by Agnès Varda • 1970 • United States', 'Agnès Varda turns her camera on an Oakland demonstration against the imprisonment of activist and Black Panthers cofounder Huey P. Newton. In addition to evincing Varda’s fascination with her adopted surroundings and her empathy, this perceptive short is also a powerful political statement.', 'Restored by the Cineteca di Bologna at L’Immagine Ritrovata in association with Ciné-Tamaris and The Film Foundation. Restoration funding provided by the Annenberg Foundation, the Los Angeles County Museum of Art (LACMA) and The Film Foundation.']
    country, descr, director, stars, year = CriterionMovieParse.extract_info_len3(info)
    assert country == ' United States'
    assert descr =='Agnès Varda turns her camera on an Oakland demonstration against the imprisonment of activist and Black Panthers cofounder Huey P. Newton. In addition to evincing Varda’s fascination with her adopted surroundings and her empathy, this perceptive short is also a powerful political statement.' + "\n\n" + 'Restored by the Cineteca di Bologna at L’Immagine Ritrovata in association with Ciné-Tamaris and The Film Foundation. Restoration funding provided by the Annenberg Foundation, the Los Angeles County Museum of Art (LACMA) and The Film Foundation.'
    assert director =='Directed by Agnès Varda '
    assert stars == ''
    assert year == '1970'


def test_extract_info_len2():
    info = ['Directed by Joel Coen and Ethan Coen • 1984 • United States', "Joel and Ethan Coen's career-long darkly comic road trip through misfit America began with this razor-sharp, hard-boiled neonoir set somewhere in Texas, where a sleazy bar owner releases a torrent of violence with one murderous thought. Actor M. Emmet Walsh looms over the proceedings as a slippery private eye with a yellow suit, a cowboy hat, and no moral compass, and Frances McDormand's cunning debut performance set her on the road to stardom. The tight scripting and inventive style that have marked the Coens' work for decades are all here in their first film, in which cinematographer Barry Sonnenfeld abandons black-and-white chiaroscuro for neon signs and jukebox colors that combine with Carter Burwell's haunting score to lurid and thrilling effect. Blending elements from pulp fiction and low-budget horror flicks, BLOOD SIMPLE reinvented the film noir for a new generation, marking the arrival of a filmmaking ensemble that would transform the American independent cinema scene."]
    country, descr, director, year = CriterionMovieParse.extract_info_len2(info)
    assert country == ' United States'
    assert descr == "Joel and Ethan Coen's career-long darkly comic road trip through misfit America began with this razor-sharp, hard-boiled neonoir set somewhere in Texas, where a sleazy bar owner releases a torrent of violence with one murderous thought. Actor M. Emmet Walsh looms over the proceedings as a slippery private eye with a yellow suit, a cowboy hat, and no moral compass, and Frances McDormand's cunning debut performance set her on the road to stardom. The tight scripting and inventive style that have marked the Coens' work for decades are all here in their first film, in which cinematographer Barry Sonnenfeld abandons black-and-white chiaroscuro for neon signs and jukebox colors that combine with Carter Burwell's haunting score to lurid and thrilling effect. Blending elements from pulp fiction and low-budget horror flicks, BLOOD SIMPLE reinvented the film noir for a new generation, marking the arrival of a filmmaking ensemble that would transform the American independent cinema scene."
    assert director == 'Directed by Joel Coen and Ethan Coen '
    assert year == ' 1984 '


def test_sanitize_data():
    country = ' United States'
    director = 'Directed by Joel Coen and Ethan Coen '
    length = 'Blood Simple\n' + '•\n' + '1h 35m'
    stars = ""
    title = 'Blood Simple'
    year = ' 1984 '
    ocountry, odirector, olength, ostars, otitle, ojust_title \
        = CriterionMovieParse.sanitize_data(country, director, length, stars, title, year)
    assert ocountry == 'United States'
    assert odirector == 'Joel Coen;Ethan Coen'
    assert olength == '1h 35m'
    assert ostars == ''
    assert otitle == 'Blood Simple (1984)'
    assert ojust_title == 'Blood Simple'


def test_sanitize_data_2():
    country = ' United States'
    director = 'Directed by Agnès Varda '
    length = 'Black Panthers\n' + '•\n' + '28m'
    stars = ''
    title = 'Black Panthers'
    year = '1970'
    ocountry, odirector, olength, ostars, otitle, ojust_title \
        = CriterionMovieParse.sanitize_data(country, director, length, stars, title, year)
    assert ocountry == 'United States'
    assert odirector == 'Agnès Varda'
    assert olength == '28m'
    assert ostars == ''
    assert otitle == 'Black Panthers (1970)'
    assert ojust_title == 'Black Panthers'


def test_sanitize_data_3():
    country = ' Australia, United States'
    director = 'Directed by Richard Franklin '
    length = 'Road Games\n' + '•\n' + '1h 40m'
    stars = 'Starring Stacy Keach, Jamie Lee Curtis, Marion Edward'
    title = 'Road Games'
    year = '1981'
    ocountry, odirector, olength, ostars, otitle, ojust_title \
        = CriterionMovieParse.sanitize_data(country, director, length, stars, title, year)
    assert ocountry == 'Australia; United States'
    assert odirector == 'Richard Franklin'
    assert olength == '1h 40m'
    assert ostars == 'Stacy Keach; Jamie Lee Curtis; Marion Edward'
    assert otitle == 'Road Games (1981)'
    assert ojust_title == 'Road Games'

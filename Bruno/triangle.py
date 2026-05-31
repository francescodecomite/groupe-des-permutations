import drawsvg as draw
from dataclasses import dataclass
import math

angle_iso = math.asin(2/3) * 360 /math.pi
unit = 100
triangle = ((0, 0), (4 * unit, 0), (2 * unit, math.sqrt(5) * unit))
style_text = '''
    font-family: monospace;
    font-weight : bold;
    font-size  : 25pt;
    fill : darkblue;
'''
style_contour = '''
    stroke : black;
    stroke-width : 1pt;
    fill : none;
'''

def reduced_triangle(p, pcent=10) :
    reduce_x  = pcent * p[1][0] /100
    reduce_y  = pcent * p[2][1] /100
    return ((reduce_x/2,reduce_y*(3/8)), (p[1][0]-reduce_x/2,reduce_y*(3/8)), (p[2][0],p[2][1]-reduce_y*(5/8)))


@dataclass(frozen=True)
class Face:
    """
        Face du TetrakiHexaèdre (sommet du graphe)
    """
    content: tuple or str;
    orient: bool = True;

    def __str__(self):
        return f"{self.content} ({self.orient})"

    def __repr__(self):
        return f"{self.content} ({self.orient})"

    def size(self):
        """
        :return: nombre de faces voisines
        """
        return len(self.content)

    def ranks(self):
        """
        :return: tuple des indices des faces voisines  (arêtes du graphe)
        """
        return tuple(range(self.size())[1:])

    def neighbour(self, rank: int = 1):
        """
        :param rank: indice de transition
        :return: Face voisine
        """
        return Face(
            self.content[0:rank - 1] + self.content[rank] + self.content[rank - 1] + self.content[rank + 1:],
            not self.orient
        )

    def to_svg_obj(self, angle=0):
        """
           Produit la représentation SVG
        :param angle: angle de rotation appliqué (en degrés)
        :return: objet SVG <g> (instance de la classe draw.Group)
        """
        face = draw.Group(transform=f'rotate({angle} {triangle[2][0]} {triangle[2][1]})') #, transform_origin=f"{triangle[2][0]} {triangle[2][1]}")
        pr = reduced_triangle(triangle, 12);
        # face.append(draw.Lines(*pr[0], *[x for point in pr[1:] for x in point], stroke='red', fill='red', close=True))
        b1 = (triangle[0], pr[0], pr[2], triangle[2])
        b2 = (triangle[0], pr[0], pr[1], triangle[1])
        b3 = (triangle[1], pr[1], pr[2], triangle[2])
        if not self.orient:
            b1, b3 = b3, b1
        face.append(
            draw.Lines(*b1[0], *[x for point in b1[1:] for x in point], stroke='none', fill='lightblue', close=True)
        )
        face.append(
            draw.Lines(*b2[0], *[x for point in b2[1:] for x in point], stroke='none', fill='orange', close=True)
        )
        face.append(
            draw.Lines(*b3[0], *[x for point in b3[1:] for x in point], stroke='none', fill='lightgreen', close=True)
        )
        face.append(
            draw.Lines(*triangle[0], *[x for point in triangle[1:] for x in point], close=True, style= style_contour)
        )
        face.append(
            draw.Text(text=''.join(self.content), font_size=0, x=triangle[2][0], y=triangle[2][1]*0.23,
                      text_anchor='middle', style=style_text, transform=f'rotate(180 {triangle[2][0]} {triangle[2][1]/4})'
                      )
        )

        return face

class Pyramid:
    """
        Ensemble de 4 faces formant une pyramide du tetrakihexaèdre
        (faces reliées par les transitions 1 ou 3)
    """
    faces : tuple
    def __init__(self, start_face:Face):
        l = [start_face]
        order = (1,3,1) if start_face.orient else (3,1,3)
        for i in order :
            l.append(l[-1].neighbour(i))
        self.faces = tuple(l)

    def neighbour_faces(self) :
        """
         Faces voisines
        :return: tuple formé des 4 faces extérieures voisines de celles de la pyramide
        """
        return tuple(f.neighbour(2) for f in self.faces)

    def to_svg_obj(self,transf : str='') :
        """
           Produit la représentation SVG
        :param transf :  attribut transform appliqué
        :return: objet SVG <g> (instance de la classe draw.Group)
        """
        pyramid = draw.Group(transform= transf)
        for count,f in enumerate(self.faces) :
            pyramid.append(f.to_svg_obj(angle=count * angle_iso))
        return pyramid



def separated_pyramids() :
    """
         groupe SVG représentant les 6 pyramides séparées les unes des autres
        :return: instance de draw.Group
    """
    g = draw.Group(transform='translate(100,50)')
    p = Pyramid(Face('abcd'))
    p_last = Pyramid(Pyramid(p.neighbour_faces()[0]).neighbour_faces()[2])
    pyramides = [p, *( Pyramid(voisine) for voisine in p.neighbour_faces()), p_last]
    for count,pf in enumerate(pyramides):
        g.append(pf.to_svg_obj(f'translate({(count%2)*600},{(count//2)*600})'))
    return g

def assembled_pyramids():
    """
     groupe SVG représentant les 6 pyramides assemblées
    :return: instance de draw.Group
    """
    g = draw.Group(transform='translate(600,1000)')
    p = Pyramid(Face('abcd'))
    p_last = Pyramid(Pyramid(p.neighbour_faces()[0]).neighbour_faces()[2])
    g.append(p.to_svg_obj())
    for i,voisine in enumerate(p.neighbour_faces()) :
        pv = Pyramid(voisine)
        g.append(pv.to_svg_obj(f'rotate({i * angle_iso} 200 223) rotate(180 200 0)'))

    g.append(p_last.to_svg_obj(f'rotate(180 200 0) rotate({2 * angle_iso} 200 223) rotate(180 200 0)'))
    return g


d = draw.Drawing(2000, 3600)
d.append(separated_pyramids());
d.save_svg('separated.svg')

d = draw.Drawing(2000, 3600)
d.append(assembled_pyramids());
d.save_svg('assembled.svg')


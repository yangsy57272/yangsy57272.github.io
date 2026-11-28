"""Selected work. Claims and media are drawn from the portfolio archive and linked papers."""

PROJECTS = [
    dict(slug='scentsense', title='ScentSense', category='Computer vision / Physical computing',
         premise='What happens when a machine’s guess becomes something you can smell?',
         image='assets/evidence/scentsense-hardware.jpg', alt='The ScentSense prototype with its scent tubes and electronics exposed',
         evidence='ScentSense prototype on the workbench', style='scent',
         study_image='assets/evidence/scentsense-cad-front.jpg', study_caption='CAD study for the four-channel enclosure',
         sections=[
             ('The device', 'My partner and I built a device that routes a facial-expression prediction to one of four scent channels. I wrote the software, connected the camera and scent channels to a Raspberry Pi, and worked through eight iterations of the housing.'),
             ('A steadier prediction', 'The scent initially changed with each new frame. I added a vote across five frames before switching. That made the output steadier during the demonstration, where one student told me they were tired after the system read their expression as sad.'),
             ('Room for a correction', 'A future interface could give the visitor a way to correct the label or choose the scent directly. The demonstration gave me a concrete reason to put that choice in the visitor’s hands.'),
         ], links=[('See the casing, model and error map', 'archive.html#scentsense')]),
    dict(slug='no-three-in-a-line', title='No three in a line', category='Combinatorics / Research',
         premise='A grid of dots, a surprisingly short bound, and the proof behind it.',
         image='assets/evidence/no-three-grid-transform.jpg', alt='A figure from the paper showing transformations of points on a grid',
         evidence='Grid transformations from the research paper', style='grid-study',
         study_image='assets/evidence/no-three-symmetry.jpg', study_caption='A grid under the paper’s symmetry operations',
         sections=[
             ('The question', 'How many points fit on a three-row grid if no straight line can pass through three of them? Each row can hold at most two points. Each column can hold at most two as well. Together these give the upper bound min(6, 2n) for n columns.'),
             ('From drawing to proof', 'Numbering the columns made a diagonal through three rows easier to detect. With equally spaced rows, the middle column must be the average of the other two. I wrote Python to enumerate configurations up to twenty columns and used explicit constructions and counting to prove the bound is attainable.'),
             ('Try the small case', 'The Playground gives you a three-by-five board to test the same constraint. A conflicting move draws the line through all three points, including diagonals that skip columns.'),
         ], links=[('Try the grid puzzle', 'playground.html#no-three-puzzle'), ('Read the research paper (PDF)', 'assets/No-Three-In-Line.pdf'), ('Browse the proof diagrams', 'archive.html#no-three')]),
    dict(slug='himcm', title='HiMCM', category='Mathematical modeling / Team research',
         premise='Two models for decisions under constraints, from computing footprints to building sweeps.',
         image='assets/activities/himcm-plan.jpg', alt='A working plan from the HiMCM team’s modeling process',
         evidence='A working page from the modeling process', style='model',
         study_image='assets/activities/himcm-equations.jpg', study_caption='Working equations from the sweep model',
         sections=[
             ('2024 · The footprint of computing', 'As team captain, I worked with my teammates to follow high-performance computing through manufacturing, transport, use and disposal. We modeled carbon emissions and water consumption, then explored how hardware replacement and electricity sources could change the footprint by 2030.'),
             ('2025 · A building sweep under changing visibility', 'Our four-person team modeled how responders search rooms as smoke spreads and visibility changes. I helped the team align on a floor plan and time step before we combined our work. Within the simulation, a sweep that prioritized the most dangerous floor could take longer overall. The team earned a finalist designation.'),
             ('What the assumptions control', 'The model held smoke behavior fixed when a door opened. Before using the model to recommend a route, I would test how changing that assumption affects who is reached first and how long a sweep takes.'),
         ], links=[('Read the 2024 paper (PDF)', 'assets/HiMCM-2024-Paper.pdf'), ('Read the 2025 paper (PDF)', 'assets/HiMCM-2025-Paper.pdf'), ('Finalist certificate (PDF)', 'assets/HiMCM-2025-Certificate.pdf'), ('Browse the 2024 footprint figures', 'archive.html#himcm-2024'), ('Browse the 2025 simulation figures', 'archive.html#himcm-2025')]),
    dict(slug='greenvolt-spark', title='Greenvolt Spark', category='Energy harvesting / Prototyping',
         premise='Exploring whether wave motion could power a coastal monitoring device.',
         image='assets/evidence/greenvolt-generator.jpg', alt='The Greenvolt Spark generator rig and its wiring',
         evidence='The physical wave-energy generator rig', style='wave',
         study_image='assets/evidence/greenvolt-wiring.jpg', study_caption='Inside the generator assembly',
         sections=[
             ('The question', 'My teammate and I built a prototype to explore whether energy harvested from waves could power coastal warning sensors.'),
             ('Building and presenting', 'I led the market research and business planning, designed parts in CAD, and assembled the prototype. My teammate focused on the engineering principles and technical feasibility. We presented the work together at the Conrad Challenge and received a silver medal.'),
             ('The next experiment', 'A reviewer suggested putting the device in a wave tank. That would give us a way to observe the prototype under more realistic wave conditions and test its suitability for monitoring.'),
         ], links=[('Browse the rig, electronics and exhibition photos', 'archive.html#greenvolt')]),
]

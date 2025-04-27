import json
import os

CONTENT_DIR = 'content'
TEMPLATE_DIR = 'templates'
OUTPUT_DIR = '..'
ASSETS_OUTPUT_DIR = 'assets'

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_OUTPUT_DIR, exist_ok=True)


with open(os.path.join(TEMPLATE_DIR, 'base.html'), 'r') as f:
   base_template = f.read()


class Page:
   def __init__(self, input_id, output_filename, active_id, group_name=None):
      self.input_id = input_id  # (str) name of file/project
      self.output_filename = output_filename  # (str)
      self.active_id = active_id  # (str) active page identifier (use for menu highlight)
      self.group_name = group_name  # (str or None) projects submenu? other submenu?

      self.content_file_path = None  # (str)
      self.metadata_file_path = None  # (str)

      self.metadata = None  # (dict) metadata from JSON
      self.content = None  # (str) (HTML) loaded content
      self.sidebar_html = None  # (str) (HTML)

   def load_paths(self):
      try:
         if self.group_name == 'projects':
            self.content_file_path = os.path.join(CONTENT_DIR, 'projects', self.input_id, 'content.html')
            self.metadata_file_path = os.path.join(CONTENT_DIR, 'projects', self.input_id, 'meta.json')
         else:
            self.content_file_path = os.path.join(CONTENT_DIR, self.input_id + '.html')
            self.metadata_file_path = os.path.join(CONTENT_DIR, self.input_id + '.json')
      except FileNotFoundError as e:
         print(f'[ERROR] Missing file for {self.input_id}: {e}')

   def load_metadata(self):
      try:
         # read metadata and content , json
         with open(self.metadata_file_path, 'r') as f:
            self.metadata = json.load(f)
         with open(self.content_file_path, 'r') as f:
            self.content = f.read()
      except json.JSONDecodeError as e:
         print(f'[ERROR] Invalid json for {self.input_id}: {e}')

   # def make_submenu(self):
   #    submenu = []
   #    for page in PAGES:
   #       if page.group_name == 'projects':
   #          active_str = 'class="active"' if page.active_id == self.metadata['active'] else ''
   #          submenu.append(f'<a href="/{page.output_filename}" {active_str}>{page.input_id.upper()}</a>')
   #    self.submenu_html = '\n'.join(submenu)

   def write_template(self):
      self.template = base_template
      self.template = self.template.replace('{{ title }}', self.metadata['title'])
      self.template = self.template.replace('{{ content }}', self.content)
      self.template = self.template.replace('{{ sidebar }}', self.sidebar_html)
      for page in PAGES:
         active_str = 'class="active"' if page.active_id == self.metadata['active'] else ''
         self.template = self.template.replace('{{ active }}', active_str)

   def save(self):
      with open(os.path.join(OUTPUT_DIR, page.output_filename), 'w') as f:
         f.write(self.template)
      print(f'Generated {page.output_filename}')

   def make_sidebar(self):
      sidebar_links = []

      # Top links
      sidebar_links.append(self._make_link('index.html', 'main page'))

      sidebar_links.append('<div>/PROJECTS</div>')

      # Project submenu
      project_links = []
      for page in PAGES:
         if page.group_name == 'projects':
            active_str = 'class="active"' if page.active_id == self.metadata['active'] else ''
            project_links.append(
               '<a href="{0}" {1}>{2}</a>'.format(page.output_filename, active_str, page.input_id.upper())
            )
      sidebar_links.append('<div class="sub-menu">' + '\n'.join(project_links) + '</div>')

      # Bottom links
      sidebar_links.append(self._make_link('contact.html', 'contact'))
      sidebar_links.append(self._make_link('about.html', 'about'))

      self.sidebar_html = '\n'.join(sidebar_links)

   def _make_link(self, filename, label):
      for page in PAGES:
         if page.output_filename == filename:
            active_str = 'class="active"' if page.active_id == self.metadata['active'] else ''
            return '<a href="{0}" {1}>{2}</a>'.format(filename, active_str, label)
      return '<a href="{0}">{1}</a>'.format(filename, label)


PAGES = [
   Page('index', 'index.html', active_id='index'),
   Page('contact', 'contact.html', active_id='contact'),
   Page('about', 'about.html', active_id='about'),
   Page('project1', 'project1.html', active_id='project1', group_name='projects'),
   Page('project2', 'project2.html', active_id='project2', group_name='projects'),
]


for page in PAGES:
   page.load_paths()
   page.load_metadata()
   page.make_sidebar()
   page.write_template()
   page.save()

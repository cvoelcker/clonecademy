import { ClonecademyPage } from './app.po';

describe('clonecademy App', () => {
  let page: ClonecademyPage;

  beforeEach(() => {
    page = new ClonecademyPage();
  });

  it('should display welcome message', done => {
    page.navigateTo();
    page.getParagraphText()
      .then(msg => expect(msg).toEqual('Welcome to app!!'))
      .then(done, done.fail);
  });
});

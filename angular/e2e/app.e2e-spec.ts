import { ClonecademyClientPage } from './app.po';

describe('clonecademy-client App', () => {
  let page: ClonecademyClientPage;

  beforeEach(() => {
    page = new ClonecademyClientPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
